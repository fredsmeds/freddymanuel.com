#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining distortions - just replace the specific pattern
content = content.replace('appealsÃƒÆ\'Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢"šÂ¬Ã‚Âa key', 'appeals—a key')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed appeals distortion')
