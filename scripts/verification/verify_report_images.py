import os
import re
from PIL import Image

with open('Report_Website/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find all img tags with src
matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', text)
print(f"Total img tags in index.html: {len(matches)}")

missing_count = 0
for src in matches:
    if not src:
        continue  # dynamic modal image placeholder
    path = os.path.join('Report_Website', src)
    if os.path.isfile(path):
        im = Image.open(path)
        print(f"[EXISTS] {src} -> dimensions {im.size}, size {os.path.getsize(path):,} bytes")
    else:
        print(f"[MISSING] {src}")
        missing_count += 1

print("="*60)
if missing_count == 0:
    print("ALL IMAGES VALIDATED AND SUCCESSFULLY PRESENT!")
else:
    print(f"WARNING: {missing_count} images missing!")
