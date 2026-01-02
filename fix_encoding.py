#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Read the index.html file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find and replace distorted UTF-8 sequences
# The pattern represents: various corrupted em-dash sequences

# List of distorted patterns and their corrections
replacements = [
    (r'existenceÃƒÂ¢Ã¢"šÂ¬', 'existence—'),
    (r'elephantÃƒÂ¢Ã¢"šÂ¬', 'elephant—'),
    (r'seemedÃƒÂ¢Ã¢"šÂ¬', 'seemed—'),
    (r'realizationÃƒÂ¢Ã¢"šÂ¬', 'realization—'),
    (r'skylineÃƒÂ¢Ã¢"šÂ¬', 'skyline—'),
    (r'portalÃƒÂ¢Ã¢"šÂ¬', 'portal—'),
    (r'materialÃƒÂ¢Ã¢"šÂ¬', 'material—'),
    (r'tonerÃƒÂ¢Ã¢"šÂ¬', 'toner—'),
    # Complex distortions - use raw bytes search
    (r"continuationÃƒÆ'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢\"šÂ¬Ã‚Â", 'continuation—'),
    (r"consequenceÃƒÆ'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢\"šÂ¬Ã‚Â", 'consequence—'),
    (r"openÃƒÆ'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢\"šÂ¬Ã‚Â", 'open—'),
]

count = 0
for distorted, corrected in replacements:
    if distorted in content:
        content = content.replace(distorted, corrected)
        count += 1
        print(f"✓ Fixed: {distorted[:40]}... → {corrected}")

# Additional regex-based replacements for complex patterns
# Match patterns like: 'or rather'
content = re.sub(r'continuation.{20,40}or rather', 'continuation—or rather', content, flags=re.DOTALL)
content = re.sub(r'consequence.{20,40}of my', 'consequence—of my', content, flags=re.DOTALL)
content = re.sub(r'open.{20,40}a cacophony', 'open—a cacophony', content, flags=re.DOTALL)

# Write back to file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal fixes applied: {count}")
print("File updated successfully!")
