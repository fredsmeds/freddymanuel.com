#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open('index.html', 'rb') as f:
    content = f.read()

# Work with the bytes directly to find and replace the distorted sequences
# The distorted pattern appears to be: [some char]ÃƒÆ'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Â[next char]
# This should be replaced with [char]—[next char]

# Convert to string for easier manipulation
content_str = content.decode('utf-8', errors='replace')

# List of all distorted patterns found in the user's text
replacements = [
    # Pattern: word + distortion + word
    ('appealsÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âa', 'appeals—a'),
    ('disdainÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚ÂThe', 'disdain. The'),
    ('audienceÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âyou', 'audience—you'),
    ('matchÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âa', 'match—a'),
]

count = 0
for old, new in replacements:
    if old in content_str:
        content_str = content_str.replace(old, new)
        count += 1
        print(f'✓ Fixed: {old[:40]}... -> {new}')

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content_str)

print(f'\nTotal fixes: {count}')
if count == 0:
    print('No remaining distortions found - file is clean!')
