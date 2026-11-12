#!/usr/bin/env python3
"""Release metadata/inventory checks only; no model or GitHub calls."""
from pathlib import Path
import hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def check(condition, message):
    if not condition: errors.append(message)
check((ROOT/'VERSION').read_text().strip()=='1.0.0','VERSION mismatch')
manifest=json.loads((ROOT/'audit/release-provenance.json').read_text())
for entry in manifest['runtime_files']:
    payload=(ROOT/entry['path']).read_bytes()
    check(hashlib.sha256(payload).hexdigest()==entry['release_sha256'],entry['path']+' checksum mismatch')
    normalized=payload.replace(b'version: "1.0.0"',b'version: "0.2.0"',1) if entry['change']=='version-metadata-only' else payload
    check(hashlib.sha256(normalized).hexdigest()==entry['source_sha256'],entry['path']+' policy change')
for rel in (ROOT/'release-files.txt').read_text().splitlines():
    p=ROOT/rel
    check(p.resolve().is_relative_to(ROOT.resolve()),'unsafe inventory path: '+rel)
    check(p.is_file(),'missing file: '+rel)
    check(not p.is_symlink(),'symlink: '+rel)
    check(not any(part in {'.git','.venv','__pycache__'} for part in Path(rel).parts),'excluded path: '+rel)
    check(not Path(rel).name.startswith('.env'),'environment file: '+rel)
    if p.is_file():
        data=p.read_bytes()
        for label,pattern in [('private key',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),('GitHub token',rb'gh[pousr]_[A-Za-z0-9]{30,}'),('AWS access key',rb'AKIA[0-9A-Z]{16}')]:
            check(not re.search(pattern,data),label+' pattern: '+rel)
check(not errors, 'release checks failed')
print(json.dumps({'passed':not errors,'errors':errors,'scope':'metadata, runtime provenance, inventory and limited secret-pattern checks; not a security guarantee'},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
