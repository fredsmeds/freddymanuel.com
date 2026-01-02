#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

with open('index.html', 'rb') as f:
    content_bytes = f.read()

# Decode and work with the content
content = content_bytes.decode('utf-8', errors='replace')

# Try aggressive replacement approach - look for the actual byte patterns
# These distortions appear to be UTF-8 encoded text being decoded as Latin-1 then re-encoded

# Find and replace: "continuation" followed by garbled chars and "or rather"  
content = content.replace('continuationÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âor rather', 'continuation—or rather')

# Find and replace: "consequence" followed by garbled chars and "of"
content = content.replace('consequenceÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âof my', 'consequence—of my')

# Find and replace: "open" followed by garbled chars and "a cacophony"
content = content.replace('openÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âa cacophony', 'open—a cacophony')

# Save back to file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed remaining distortions!")
