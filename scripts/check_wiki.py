#!/usr/bin/env python3
"""Basic deterministic checks. Not a substitute for scientific claim validation."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'docs' / 'sources.json'


def main():
    entries = json.loads(SOURCES.read_text(encoding='utf-8'))
    ids = [row['id'] for row in entries]
    errors = []
    if len(ids) != len(set(ids)):
        errors.append('Duplicate source IDs')
    if len(entries) < 5:
        errors.append('Fewer than five registered sources')
    valid_status = {'planned', 'in_progress', 'ingested', 'verified'}
    for row in entries:
        if row['status'] not in valid_status:
            errors.append(f"Invalid source status: {row['id']}")
        if row['status'] in {'ingested','verified'} and not (ROOT/'wiki'/'sources'/f"{row['id']}.md").is_file():
            errors.append(f"Missing source record for {row['id']}")
    md = list((ROOT/'wiki').rglob('*.md'))
    link_pattern = re.compile(r'(?<!!)\[[^]]+\]\(([^)]+)\)')
    for path in md:
        for target in link_pattern.findall(path.read_text(encoding='utf-8')):
            target = target.split('#', 1)[0]
            if target and not target.startswith(('https://','http://','mailto:')) and not (path.parent/target).exists():
                errors.append(f'Broken local link: {path.relative_to(ROOT)} -> {target}')
    ingested = sum(x['status'] in {'ingested','verified'} for x in entries)
    verified = sum(x['status'] == 'verified' for x in entries)
    print(f'Sources registered: {len(entries)} | ingested or verified: {ingested} | verified: {verified} | Wiki Markdown files: {len(md)}')
    for error in errors:
        print('ERROR:', error)
    if errors:
        sys.exit(1)
    print('Scaffold checks: PASS (does NOT establish source ingestion or factual accuracy)')


if __name__ == '__main__':
    main()
