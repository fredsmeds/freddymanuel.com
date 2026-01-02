#!/usr/bin/env python
# Binary-level fix for distorted text

with open('index.html', 'rb') as f:
    data = f.read()

# The actual corrupted bytes in the file (from the binary inspection)
# "appeals" followed by distorted bytes that should be "—"
# Let me search for different patterns

# Try to find and fix by looking at the actual bytes
original = data

# Pattern 1: appeals followed by corrupted dash
# Looking for: appeals + [corrupted] + a key
patterns = [
    (b'appeals\xc3\x83\xc6\x92\xc3\x82\xc2\xa2\xc3\x83\xc2\xa2\xc3\xa2\xe2\x80\x9a\xc2\xb1\xc3\x82\xc2\xac\xc3\x83\xc2\xa2\xc3\xa2\xe2\x80\x9c\xc5\xa1\xc2\xac\xc3\x82\xc2\xa2a key', b'appeals\xe2\x80\x94a key'),
    # Alternative patterns with different encodings
    (b'appeals\xc3\x83\xc6\x92\xc3\x82\xc2\xa2\xc3\x83\xc2\xa2\xc3\xa2\xe2\x80\x9a\xc2\xb1\xc3\x82\xc2\xac\xc3\x83\xc2\xa2\xc3\xa2\xe2\x80\x9c\xc5\xa1\xc2\xac\xc3\x82\xc2\xac a key', b'appeals\xe2\x80\x94a key'),
]

fixed_count = 0
for old_pattern, new_pattern in patterns:
    if old_pattern in data:
        data = data.replace(old_pattern, new_pattern)
        fixed_count += 1
        print(f"Fixed pattern")

# Try another approach - look for the text after "appeals"
# Find position of "appeals"
idx = data.find(b'appeals')
if idx != -1:
    # Look at what comes after
    context = data[idx:idx+100]
    print(f"Context around appeals: {context}")
    
    # Find the next "a key"
    next_a_key_idx = data.find(b'a key', idx + 7)
    if next_a_key_idx != -1:
        print(f"Found 'a key' at offset {next_a_key_idx - idx} from 'appeals'")
        # The gap should be just a dash
        between = data[idx+7:next_a_key_idx]
        print(f"Between appeals and 'a key': {between}")
        print(f"Hex: {between.hex()}")
        
        # Replace just this section
        data = data[:idx+7] + b'\xe2\x80\x94' + data[next_a_key_idx:]
        fixed_count += 1

if data != original:
    with open('index.html', 'wb') as f:
        f.write(data)
    print(f"File fixed! ({fixed_count} replacements)")
else:
    print("No changes made")
