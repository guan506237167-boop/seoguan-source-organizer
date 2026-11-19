"""Offline, conservative source-ledger normalization. Python 3.10+."""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def normalize_url(raw):
    raw = raw.strip()
    if any(ord(c) < 32 or c.isspace() for c in raw):
        raise ValueError('URL contains whitespace or controls')
    p = urlsplit(raw)
    if p.scheme.lower() not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('Expected HTTP(S) URL without credentials')
    host = p.hostname.lower()
    if ':' in host:
        host = '[' + host + ']'
    else:
        host = host.encode('idna').decode('ascii')
    port = p.port
    if port is not None and port != (443 if p.scheme.lower() == 'https' else 80):
        host += ':' + str(port)
    # Preserve path, query and fragment: they may distinguish evidence locations.
    return urlunsplit((p.scheme.lower(), host, p.path, p.query, p.fragment))


def organize(rows):
    groups = {}
    invalid = []
    for line, row in enumerate(rows, 2):
        try:
            url = normalize_url(row.get('url') or '')
        except (ValueError, UnicodeError) as e:
            invalid.append({'line': line, 'raw_url': row.get('url'), 'error': str(e)})
            continue
        identity = tuple((row.get(k) or '').strip() for k in ('record_id', 'platform', 'question_id', 'location'))
        # Unknown provenance is not an empty identity shared by every unknown row.
        key = (*identity, url, line if not all(identity) else None)
        if key in groups:
            groups[key]['source_lines'].append(line)
            groups[key]['raw_urls'].append(row['url'])
            groups[key]['original_rows'].append({'line': line, 'fields': dict(row)})
            for field, value in row.items():
                if field != 'url' and groups[key].get(field) != value:
                    conflict = groups[key]['metadata_conflicts'].setdefault(field, [groups[key].get(field)])
                    if value not in conflict:
                        conflict.append(value)
        else:
            groups[key] = {**row, 'normalized_url': url, 'host': urlsplit(url).hostname,
                           'raw_urls': [row['url']], 'source_lines': [line],
                           'original_rows': [{'line': line, 'fields': dict(row)}], 'metadata_conflicts': {},
                           'provenance_complete': all(identity)}
    result = list(groups.values())
    return {'rows': result, 'unique_urls': sorted({r['normalized_url'] for r in result}),
            'invalid': invalid, 'network_checked': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    try:
        with a.input.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            required = {'record_id', 'platform', 'question_id', 'url', 'location'}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError('CSV requires: ' + ','.join(sorted(required)))
            result = organize(reader)
        with a.output.open('x', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps({'rows': len(result['rows']), 'invalid': len(result['invalid'])}))
    except (OSError, ValueError, csv.Error) as e:
        p.exit(2, str(e) + '\n')


if __name__ == '__main__':
    main()
