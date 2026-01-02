#!/usr/bin/env python
# Fix the distorted "appeals" text

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# List of all distortions the user reported - fixing them directly
fixes = [
    # Line 802-803 - appeals
    ('appealsÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âa key', 'appeals—a key'),
    
    # Line 689-690 - continuation and consequence
    ('continuationÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Â', 'continuation—'),
    ('consequenceÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Â', 'consequence—'),
    
    # Line 691 - open
    ('openÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âtabs', 'open—tabs'),
    
    # Line 824 - match
    ('matchÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âa', 'match—a'),
    
    # Line 993 - elephant (already fixed)
    # Line 1090 - portal (already fixed) 
    # Line 1268 - might have issues too
]

count = 0
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"Fixed: {old[:30]}... → {new}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal replacements: {count}")
