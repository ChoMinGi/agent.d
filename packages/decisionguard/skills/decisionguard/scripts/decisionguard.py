#!/usr/bin/env python3
"""Offline evidence checks. No network, credentials, or external write operations."""
import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit


class ValidationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def text_field(obj, key):
    value = obj.get(key)
    require(isinstance(value, str) and bool(value.strip()), f"{key}: nonempty string required")
    return value


def object_list(obj, key, nonempty=False):
    value = obj.get(key)
    require(isinstance(value, list) and all(isinstance(v, dict) for v in value),
            f"{key}: list of objects required")
    require(not nonempty or bool(value), f"{key}: cannot be empty")
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(result.tzinfo is not None, "fetched_at: timezone required")
    except (ValueError, AttributeError) as exc:
        raise ValidationError("fetched_at: ISO timestamp with timezone required") from exc


def status_source(record, sources):
    sid = record.get("status_source_id", record["source_id"])
    require(isinstance(sid, str) and sid in sources, "status evidence source is missing")
    source = sources[sid]
    origin = sources[record["source_id"]]
    if sid != origin["id"]:
        require(isinstance(origin.get("project_id"), str) and
                source.get("project_id") == origin["project_id"], "status evidence must be in the same project")
    require(record["status_quote"] in source["content"], "status quote is absent from source")
    return source


def validate_snapshot(snapshot):
    require(isinstance(snapshot, dict), "snapshot: object required")
    require(type(snapshot.get("schema_version")) is int and snapshot["schema_version"] == 1,
            "snapshot: schema_version must be 1")
    coverage = snapshot.get("coverage")
    require(isinstance(coverage, dict), "coverage: object required")
    text_field(coverage, "scope")
    require(type(coverage.get("complete")) is bool, "coverage.complete: boolean required")
    require(isinstance(coverage.get("gaps"), list) and
            all(isinstance(g, str) and g.strip() for g in coverage["gaps"]),
            "coverage.gaps: list of nonempty strings required")
    sources = {}
    for source in object_list(snapshot, "sources"):
        for field in ("id", "title", "url", "revision", "content", "fetched_at"):
            text_field(source, field)
        timestamp(source["fetched_at"])
        url = urlsplit(source["url"])
        require(url.scheme in {"https", "demo"} and bool(url.netloc)
                and not url.username and not url.password, "source URL: https or demo URL required")
        require(type(source.get("complete")) is bool, "source.complete: boolean required")
        require(source["id"] not in sources, "duplicate source ID")
        sources[source["id"]] = source
    decisions = {}
    for decision in object_list(snapshot, "decisions"):
        for field in ("id", "key", "scope", "value", "status", "source_id", "quote", "status_quote"):
            text_field(decision, field)
        require(decision["id"] not in decisions, "duplicate decision ID")
        require(decision["status"] in {"accepted", "draft", "superseded", "rejected", "expired", "unknown"},
                "unsupported decision status")
        require(decision["source_id"] in sources, "decision refers to a missing source")
        source = sources[decision["source_id"]]
        require(decision["quote"] in source["content"], "decision quote is absent from source")
        status_source(decision, sources)
        decisions[decision["id"]] = decision
    for decision in decisions.values():
        successor = decision.get("superseded_by")
        if successor is not None:
            require(decision["status"] == "superseded", "only superseded decisions can name a successor")
            require(successor in decisions and successor != decision["id"], "missing or self successor")
            new = decisions[successor]
            require(new["status"] == "accepted" and (new["key"], new["scope"]) ==
                    (decision["key"], decision["scope"]), "successor must be accepted in the same scope/key")
            require(sources[new["source_id"]]["complete"], "successor source is incomplete")
            require(status_source(new, sources)["complete"], "successor authority source is incomplete")
        elif decision["status"] == "superseded":
            raise ValidationError("superseded decision requires a verified successor")
    for impact in object_list(snapshot, "impacts"):
        for field in ("decision_id", "source_id", "quote"):
            text_field(impact, field)
        require(impact["decision_id"] in decisions, "impact refers to a missing decision")
        require(impact["source_id"] in sources, "impact refers to a missing source")
        require(impact["quote"] in sources[impact["source_id"]]["content"], "impact quote absent from source")
    return sources, decisions


def citation(source, quote):
    return {key: source[key] for key in ("id", "title", "url", "revision", "fetched_at")} | {"quote": quote}


def review(snapshot, proposal):
    sources, decisions = validate_snapshot(snapshot)
    require(isinstance(proposal, dict), "proposal: object required")
    text_field(proposal, "summary")
    claims = object_list(proposal, "claims", nonempty=True)
    seen = set()
    for claim in claims:
        for field in ("key", "scope", "value"):
            text_field(claim, field)
        pair = (claim["key"], claim["scope"])
        require(pair not in seen, "duplicate proposal scope/key")
        seen.add(pair)
    gaps = list(snapshot["coverage"]["gaps"])
    if not snapshot["coverage"]["complete"]:
        gaps.append("Search coverage is incomplete.")
    findings, checked, relevant = [], [], set()
    for claim in claims:
        matching = [d for d in decisions.values() if (d["key"], d["scope"]) ==
                    (claim["key"], claim["scope"])]
        accepted = []
        for decision in matching:
            source = sources[decision["source_id"]]
            if not source["complete"] or not status_source(decision, sources)["complete"]:
                gaps.append(f"Incomplete source for {decision['id']}.")
                continue
            if decision["status"] == "unknown":
                gaps.append(f"Unverified authority for {decision['id']}.")
            if decision["status"] == "accepted":
                accepted.append(decision)
        if not accepted:
            gaps.append(f"No supported accepted decision for {claim['key']} in {claim['scope']}.")
        if len({d["value"] for d in accepted}) > 1:
            gaps.append(f"Accepted decisions disagree for {claim['key']} in {claim['scope']}.")
        for decision in accepted:
            source = sources[decision["source_id"]]
            relevant.add(decision["id"])
            checked.append(decision["id"])
            if decision["value"] != claim["value"]:
                findings.append({
                    "kind": "potential_conflict", "decision_id": decision["id"],
                    "key": claim["key"], "scope": claim["scope"],
                    "existing": decision["value"], "proposed": claim["value"],
                    "evidence": citation(source, decision["quote"]),
                    "status_evidence": decision["status_quote"],
                    "status_citation": citation(status_source(decision, sources), decision["status_quote"]),
                    "reason": "Different normalized values in the same explicit scope; verify semantics and exceptions.",
                })
    impacts = []
    for impact in snapshot["impacts"]:
        if impact["decision_id"] in relevant:
            source = sources[impact["source_id"]]
            if source["complete"]:
                impacts.append({"decision_id": impact["decision_id"],
                                "evidence": citation(source, impact["quote"])})
            else:
                gaps.append(f"Incomplete impact source {source['id']}.")
    return {
        "schema_version": 1, "proposal": proposal["summary"],
        "status": "potential_conflicts" if findings else "needs_context" if gaps else "no_conflict_in_checked_claims",
        "coverage": snapshot["coverage"], "checked_decisions": sorted(set(checked)),
        "findings": findings, "impacts": impacts, "gaps": list(dict.fromkeys(gaps)),
        "limitations": ["Exact normalized comparisons only; extraction and semantics require agent review.",
                        "No result establishes global consistency or authorizes a write."],
        "writes_performed": 0,
    }


def snapshot_state(snapshot):
    # Retrieval time changes on a fresh read; content, revisions and mappings must not.
    state = dict(snapshot)
    state["sources"] = sorted(
        [{k: v for k, v in s.items() if k != "fetched_at"} for s in snapshot["sources"]],
        key=lambda s: s["id"],
    )
    return digest(state)


def make_plan(snapshot, edits):
    sources, _ = validate_snapshot(snapshot)
    require(snapshot["coverage"]["complete"] and not snapshot["coverage"]["gaps"],
            "resolve evidence coverage gaps before building a commit plan")
    require(all(s["complete"] for s in sources.values()), "resolve incomplete evidence before planning")
    require(isinstance(edits, dict), "edits: object required")
    changes, targets = [], set()
    for edit in object_list(edits, "changes", nonempty=True):
        for field in ("source_id", "before", "after", "rationale"):
            text_field(edit, field)
        sid = edit["source_id"]
        require(sid in sources, "unknown edit target")
        require(sid not in targets, "one exact replacement per target per plan")
        targets.add(sid)
        source = sources[sid]
        require(source["content"].count(edit["before"]) == 1, "before text must occur exactly once")
        require(edit["before"] != edit["after"], "edit has no change")
        evidence = edit.get("evidence_ids")
        require(isinstance(evidence, list) and evidence and
                all(isinstance(i, str) and i in sources for i in evidence), "valid evidence_ids required")
        changes.append({k: edit[k] for k in ("source_id", "before", "after", "rationale")} | {
            "evidence_ids": sorted(set(evidence)), "url": source["url"],
            "expected_revision": source["revision"], "expected_content_sha256": digest(source["content"]),
        })
    body = {"schema_version": 1, "snapshot_sha256": snapshot_state(snapshot), "changes": changes}
    return body | {"plan_id": digest(body)}


def check_plan(plan, snapshot, approval):
    require(isinstance(plan, dict), "plan: object required")
    require(isinstance(approval, dict), "approval: object required")
    require(approval.get("approved") is True, "explicit confirmation record required")
    text_field(approval, "confirmed_by")
    text_field(approval, "confirmation_reference")
    require(approval.get("plan_id") == plan.get("plan_id") and isinstance(plan.get("plan_id"), str),
            "confirmation does not match this plan")
    require(make_plan(snapshot, {"changes": object_list(plan, "changes", nonempty=True)}) == plan,
            "plan changed or snapshot is stale; review and reconfirm")
    return {"status": "preflight_passed", "plan_id": plan["plan_id"], "writes_performed": 0,
            "limitation": "The host must verify actual user confirmation and perform a fresh connector read before any write."}


def load_json(path):
    def unique_keys(pairs):
        obj = {}
        for key, value in pairs:
            require(key not in obj, f"duplicate JSON key: {key}")
            obj[key] = value
        return obj
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_keys,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValidationError("nonfinite JSON number")))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, fields in {"context": ("snapshot", "task"), "review": ("snapshot", "proposal"), "plan": ("snapshot", "edits"),
                         "check": ("plan", "snapshot", "approval")}.items():
        command = sub.add_parser(name)
        for field in fields:
            command.add_argument(f"--{field}", required=True, type=Path)
        if name == "context":
            command.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    try:
        snapshot = load_json(args.snapshot)
        if args.command == "context":
            from context_prepare import prepare_context, render_markdown
            result = prepare_context(snapshot, load_json(args.task))
            if args.format == "markdown":
                print(render_markdown(result))
                return 0
        elif args.command == "review":
            result = review(snapshot, load_json(args.proposal))
        elif args.command == "plan":
            result = make_plan(snapshot, load_json(args.edits))
        else:
            result = check_plan(load_json(args.plan), snapshot, load_json(args.approval))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValidationError, OSError, ValueError, TypeError) as exc:
        print(f"decisionguard: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
