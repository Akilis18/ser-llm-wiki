#!/usr/bin/env python3
"""Validate Wiki structure and citation pointers without reading research claims."""
import json
import re
import sys
from collections import deque
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'\[[^\]\n]+\]\(([^)\n]+)\)')
ID = r'S\d{2}'
CHAPTER = re.compile(r'^# ([1-6])\. ', re.M)
EVIDENCE = re.compile(
    rf'^\| [^|\n]+ \| \[({ID})\], ([^|\n]+) \| \[[^\]\n]+\]\(([^)\n]+)\) \|$', re.M
)
CITATION = re.compile(rf'\[({ID})\]\(([^)\n]+)\), ([^\n]+)')
COMPLETE = {'ingested', 'verified'}


def markdown_files(root):
    paths = [root / name for name in ('README.md', 'AGENTS.md')]
    for folder in ('wiki', 'docs', 'logs'):
        paths.extend((root / folder).rglob('*.md'))
    return sorted(paths)


def validate(root):
    errors = []
    entries = json.loads((root / 'docs/sources.json').read_text(encoding='utf-8'))
    registry = {row['id']: row for row in entries}
    if len(entries) != len(registry):
        errors.append('Duplicate source IDs')
    if len(registry) < 5:
        errors.append('Fewer than five registered sources')

    markdown = {}
    for path in markdown_files(root):
        try:
            content = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as err:
            errors.append(f'{path.relative_to(root)}: {err}')
            continue
        if '\ufeff' in content or '\ufffd' in content:
            errors.append(f'Unexpected Unicode marker: {path.relative_to(root)}')
        markdown[path] = content

    links = {}
    for path, content in markdown.items():
        links[path] = set()
        for href in LINK.findall(content):
            target = urlsplit(href)
            if target.scheme or target.netloc or not target.path:
                continue
            destination = (path.parent / unquote(target.path)).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f'Broken local link: {path.relative_to(root)} -> {href}')
            links[path].add(destination)

    wiki = {path for path in markdown if path.is_relative_to(root / 'wiki')}
    index = root / 'wiki/index.md'
    reachable = set()
    pending = deque([index])
    while pending:
        path = pending.popleft()
        if path not in reachable:
            reachable.add(path)
            pending.extend(links.get(path, set()) & wiki)
    for path in sorted(wiki - reachable):
        errors.append(f'Orphan Wiki page: {path.relative_to(root)}')

    chapters = {}
    for path in sorted(wiki):
        heading = CHAPTER.match(markdown[path])
        if heading:
            number = int(heading[1])
            if number in chapters:
                errors.append(f'Duplicate teaching chapter {number}')
            chapters[number] = path
    for number in range(1, 7):
        heading = re.search(rf'^{number}\. \[[^\]\n]+\]\(([^)\n]+)\)$',
                            markdown.get(index, ''), re.M)
        if not heading or (index.parent / heading[1]).resolve() != chapters.get(number):
            errors.append(f'Missing or incorrect index entry for chapter {number}')

    evidence = set()
    observed = {sid: set() for sid in registry}
    human_registry = markdown.get(root / 'docs/02_sources.md', '')
    for sid, row in registry.items():
        status = row['status']
        if not re.fullmatch(ID, sid) or status not in COMPLETE | {'planned', 'in_progress'}:
            errors.append(f'Invalid source ID or status: {sid}')
            continue
        if status not in COMPLETE:
            continue
        record = root / 'wiki/sources' / f'{sid}.md'
        content = markdown.get(record, '')
        if record not in links.get(index, set()) or not content:
            errors.append(f'Missing indexed source record: {sid}')
        try:
            verified_on = date.fromisoformat(row['verified_on'])
        except (TypeError, ValueError):
            errors.append(f'Invalid verification date: {sid}')
            continue
        if (f'**Status** \u2014 {status} on {verified_on}.' not in content
                or row['local_file'] != f'raw/{sid}.pdf'
                or f"\x60{row['local_file']}\x60" not in content):
            errors.append(f'Source metadata differs from registry: {sid}')
        listed = ','.join(map(str, row['chapters']))
        if not re.search(
                rf'^\| \[{sid}\]\(\.\./wiki/sources/{sid}\.md\) \| [^|\n]+'
                rf' \| {listed} \| {status.title()} \|$', human_registry, re.M):
            errors.append(f'Human-readable registry differs: {sid}')
        rows = EVIDENCE.findall(content)
        if not rows:
            errors.append(f'Missing located evidence: {sid}')
        for cited, location, destination in rows:
            chapter = (record.parent / destination).resolve()
            if cited != sid or chapter not in chapters.values() or not re.search(r'\bp{1,2}\. \d', location):
                errors.append(f'Invalid evidence row in {sid}: {location}')
            evidence.add((sid, chapter, location))

    used = set()
    for number, chapter in chapters.items():
        content = markdown[chapter]
        citations = list(CITATION.finditer(content))
        if not citations or len(citations) != len(re.findall(rf'\[{ID}\]', content)):
            errors.append(f'Missing citation link or location in chapter {number}')
        for match in citations:
            sid, destination, location = match.groups()
            record = root / 'wiki/sources' / f'{sid}.md'
            if sid not in observed or (chapter.parent / destination).resolve() != record:
                errors.append(f'Invalid citation target in chapter {number}: {sid}')
                continue
            observed[sid].add(number)
            keys = {key for key in evidence
                    if key[:2] == (sid, chapter) and key[2] == location.removesuffix('.')}
            if not keys:
                errors.append(f'Citation without matching evidence in chapter {number}: {sid}, {location}')
            used.update(keys)
    for sid, chapter, location in sorted(evidence - used):
        errors.append(f'Unreferenced evidence: {sid} -> {chapter.name}, {location}')
    for sid, row in registry.items():
        if row['status'] in COMPLETE and observed[sid] != set(row['chapters']):
            errors.append(f'Chapter mapping differs from citations: {sid}')

    ingested = sum(row['status'] in COMPLETE for row in entries)
    print(f'Sources registered: {len(registry)} | ingested or verified: {ingested} | '
          f'Wiki pages: {len(wiki)} | chapters: {len(chapters)} | evidence pointers: {len(evidence)}')
    return errors


def main():
    errors = validate(ROOT)
    for error in errors:
        print('ERROR:', error)
    if errors:
        sys.exit(1)
    print('Structural checks: PASS. Research claim validation requires manual review.')


if __name__ == '__main__':
    main()
