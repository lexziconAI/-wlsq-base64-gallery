#!/usr/bin/env python3
"""Diagnostic utility for image_base64_lookup.json

Reports:
- File size
- Entry count
- Per-entry base64 length stats
- Shortest & largest entries
- Missing metadata keys (if any)
- Estimated original binary size from base64 length
"""
import json, os, math, sys
from statistics import mean
from pathlib import Path

LOOKUP_PATH = Path('image_base64_lookup.json')

if not LOOKUP_PATH.exists():
    print('File not found:', LOOKUP_PATH)
    sys.exit(1)

size_bytes = LOOKUP_PATH.stat().st_size
print(f'File: {LOOKUP_PATH} \nSize (bytes): {size_bytes:,} (~{size_bytes/1024:.1f} KB, {size_bytes/1024/1024:.2f} MB)')

with open(LOOKUP_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total top-level entries: {len(data)}')

lengths = []
records = []
for k,v in data.items():
    if isinstance(v, dict):
        b64 = v.get('base64','')
    else:
        b64 = v
    l = len(b64)
    lengths.append(l)
    # approximate original binary size = 3/4 of base64 chars (minus padding)
    approx_bin = int(l * 0.75)
    records.append((k,l,approx_bin))

if not lengths:
    print('No base64 fields found.')
    sys.exit(0)

print(f'Base64 field stats (characters including data: URI prefix):')
print(f'  Min:   {min(lengths):,}')
print(f'  Max:   {max(lengths):,}')
print(f'  Mean:  {int(mean(lengths)):,}')
print(f'  Total chars (all base64 strings): {sum(lengths):,}')

# Show 5 smallest and 5 largest
smallest = sorted(records, key=lambda r: r[1])[:5]
largest = sorted(records, key=lambda r: r[1])[-5:]
print('\nFive smallest entries:')
for k,l,bin_sz in smallest:
    print(f'  {k:35} {l:10,} chars  ~{bin_sz/1024:.1f} KB original')
print('\nFive largest entries:')
for k,l,bin_sz in largest:
    print(f'  {k:35} {l:10,} chars  ~{bin_sz/1024:.1f} KB original')

# Sanity: list any entries with suspiciously short base64 (<1000 chars)
short = [r for r in records if r[1] < 1000]
if short:
    print(f'\nEntries with unusually short base64 (<1000 chars): {len(short)}')
    for k,l,_ in short[:10]:
        print('  ', k, l)

# Check for expected keys from metadata (if CSV exists)
meta_csv = Path('WLSQ_assets_catalogue.csv')
if meta_csv.exists():
    import csv
    with open(meta_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        expected = {Path(row['filename']).stem for row in reader if row.get('filename')}
    missing = expected - set(data.keys())
    if missing:
        print(f'\nWARNING: Missing {len(missing)} metadata-derived keys:')
        for m in sorted(missing):
            print('  ', m)
    else:
        print('\nAll metadata keys are present.')
else:
    print('\nMetadata CSV not found for cross-check.')

print('\nDone.')
