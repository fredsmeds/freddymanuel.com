#!/usr/bin/env python
# Fix spacing issues in the final text

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix spacing around dashes and conjunctions
fixes = [
    ('continuationor', 'continuation—or'),
    ('consequenceof', 'consequence—of'),
]

count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f'Fixed spacing: {old} → {new}')

if count > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'\nTotal fixes: {count}')
else:
    print('No spacing issues found to fix')
