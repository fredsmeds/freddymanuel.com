#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Read the index.html file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary of all corrections
replacements = {
    # Line 993 - Internercia Performance
    'While the internet offers a sanitized, disembodied presence, the performance confronts the audience with the undeniable, biological evidence of my existence—a presence that has a scent, that sweats and decays, and that is fundamentally, messily human. It is in this sensory, uncomfortable truth that the illusion of digital connection is most profoundly broken.': 
    'While the internet offers a sanitized, disembodied presence, the performance confronts the audience with the undeniable, biological evidence of my existence—a presence that has a scent, that sweats and decays, and that is fundamentally, messily human. It is in this sensory, uncomfortable truth that the illusion of digital connection is most profoundly broken.',
    
    # Line 1090 - Park Portal
    'The final installation aimed to create an immersive world. By integrating a real, functioning lamppost that mirrored those in my illustrations, the piece intentionally blurred the line between the two-dimensional artwork and the three-dimensional space of the lounge. Ultimately, \'Park\' became a portal—a constructed dream of a London evening, created to transport guests from the heart of Dubai into a moment of borrowed nostalgia.':
    'The final installation aimed to create an immersive world. By integrating a real, functioning lamppost that mirrored those in my illustrations, the piece intentionally blurred the line between the two-dimensional artwork and the three-dimensional space of the lounge. Ultimately, \'Park\' became a portal—a constructed dream of a London evening, created to transport guests from the heart of Dubai into a moment of borrowed nostalgia.',
    
    # Line 1125 - Nepal first paragraph
    'In 2014, I spent twenty days traveling through Nepal, from the ancient cityscapes of the Kathmandu Valley to the serene lakeside of Pokhara. My initial goal was one of quiet observation, capturing the intimate moments and vast landscapes through my lens. The first part of my journey was defined by this connection—to the people I was with and the stunning, peaceful environment around us.':
    'In 2014, I spent twenty days traveling through Nepal, from the ancient cityscapes of the Kathmandu Valley to the serene lakeside of Pokhara. My initial goal was one of quiet observation, capturing the intimate moments and vast landscapes through my lens. The first part of my journey was defined by this connection—to the people I was with and the stunning, peaceful environment around us.',
    
    # Line 1140 - Nepal elephant encounter
    'The ride ended at a sanctuary, but the most profound moment occurred just beyond its boundaries. A wild male elephant—the \'king,\' as he seemed—emerged from the wilderness. He was immense, powerful, and utterly free, his tusks untouched, a stark contrast to the subjugated animals we had just left. He was the embodiment of everything I had hoped to see.':
    'The ride ended at a sanctuary, but the most profound moment occurred just beyond its boundaries. A wild male elephant—the \'king,\' as he seemed—emerged from the wilderness. He was immense, powerful, and utterly free, his tusks untouched, a stark contrast to the subjugated animals we had just left. He was the embodiment of everything I had hoped to see.',
    
    # Line 1153 - Nepal battery died
    'As I raised my camera to capture this incredible sight, my battery died. In that moment of failure, I found the true theme of my journey. The most powerful, most authentic image of my entire trip was the one I was not allowed to take. It forced me to put down the camera and simply witness. This series is not just about what I saw in Nepal, but about that moment of realization—a reflection on the image not taken, and the difference between capturing a moment and truly living it.':
    'As I raised my camera to capture this incredible sight, my battery died. In that moment of failure, I found the true theme of my journey. The most powerful, most authentic image of my entire trip was the one I was not allowed to take. It forced me to put down the camera and simply witness. This series is not just about what I saw in Nepal, but about that moment of realization—a reflection on the image not taken, and the difference between capturing a moment and truly living it.',
    
    # Line 1217 - Cosmopolitical origin
    'The origin of this project was an accident of place. I found the raw material—bottles of Cyan, Magenta, Yellow, and Black printer toner—in a crowded electronics shop in Dragon Mart. I was immediately struck by the medium: it was the elemental dust of mass media and digital reproduction. I felt I had found the very DNA of the city\'s synthetic and hypermodern landscape.':
    'The origin of this project was an accident of place. I found the raw material—bottles of Cyan, Magenta, Yellow, and Black printer toner—in a crowded electronics shop in Dragon Mart. I was immediately struck by the medium: it was the elemental dust of mass media and digital reproduction. I felt I had found the very DNA of the city\'s synthetic and hypermodern landscape.',
    
    # Line 1268 - Cosmopolitical resulting images
    'The resulting images are a direct response to this tension. The violent explosions capture the energy of cultural collision. The totemic and pillar-like shapes are my representations of the city\'s skyline—monuments that seem at once powerful and ephemeral, as if they could dissolve back into dust. In pieces like the one inspired by a traditional Emirati mask, I sought to capture the fragile beauty of a culture holding its shape against the tide of globalization. This series is my attempt to deconstruct the city, using its own language to question its nature.':
    'The resulting images are a direct response to this tension. The violent explosions capture the energy of cultural collision. The totemic and pillar-like shapes are my representations of the city\'s skyline—monuments that seem at once powerful and ephemeral, as if they could dissolve back into dust. In pieces like the one inspired by a traditional Emirati mask, I sought to capture the fragile beauty of a culture holding its shape against the tide of globalization. This series is my attempt to deconstruct the city, using its own language to question its nature.',
}

# Count replacements
count = 0
for old_text, new_text in replacements.items():
    if old_text in content:
        content = content.replace(old_text, new_text)
        count += 1

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Replacements completed: {count}")
