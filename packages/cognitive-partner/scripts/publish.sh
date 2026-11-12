#!/usr/bin/env bash
# Explicit one-time publication. Never force-push, delete, or overwrite a repository.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
REPO="ChoMinGi/cognitive-partner"
TAG="v1.0.0"
VISIBILITY="private"
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --private) VISIBILITY="private" ;;
    --public) VISIBILITY="public" ;;
    --dry-run) DRY_RUN=1 ;;
    *) echo "Usage: bash scripts/publish.sh [--private|--public] [--dry-run]" >&2; exit 2 ;;
  esac
done
if [ "$DRY_RUN" -eq 1 ]; then
  printf 'Plan only; no GitHub writes or git initialization.\nRepo: %s\nVisibility: %s\nTag: %s\n' "$REPO" "$VISIBILITY" "$TAG"
  printf 'Steps: validate -> initial commit -> create repository/push -> push tag -> create release\n'
  exit 0
fi
for tool in git gh python3; do
  command -v "$tool" >/dev/null || { echo "Missing command: $tool" >&2; exit 2; }
done
LOGIN="$(gh api user --jq '.login')"
[ "$LOGIN" = "ChoMinGi" ] || { echo "Wrong GitHub account: $LOGIN; expected ChoMinGi" >&2; exit 2; }
if git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Existing Git worktree detected. Use a fresh extracted release folder; nothing changed." >&2
  exit 2
fi
# A failed lookup may be a network/auth error. 'gh repo create' remains the final
# authority and fails rather than overwriting an existing repository.
if gh repo view "$REPO" --json name >/dev/null 2>&1; then
  echo "$REPO already exists. Refusing to overwrite or merge unrelated history." >&2
  exit 2
fi
git var GIT_AUTHOR_IDENT >/dev/null || { echo "Configure your Git author name/email first." >&2; exit 2; }
python3 -B validate_package.py
python3 -B audit/test_validator_contract.py
python3 -B scripts/check_release.py
# Use the audited file inventory; do not add unrelated files or local credentials.
FILES=()
while IFS= read -r file; do FILES+=("$file"); done < release-files.txt
git init -b main
git add -- "${FILES[@]}"
git commit -m "release: Cognitive Partner v1.0.0"
git tag -a "$TAG" -m "Cognitive Partner v1.0.0"
gh repo create "$REPO" "--$VISIBILITY" --source=. --remote=origin --push \
  --description "An Agent Skill for active human-AI reasoning and better work outcomes."
git push origin "refs/tags/$TAG"
gh release create "$TAG" --repo "$REPO" --verify-tag \
  --title "Cognitive Partner $TAG" --notes-file RELEASE_NOTES.md
gh release view "$TAG" --repo "$REPO" --json url --jq '.url'
