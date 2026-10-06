from PIL import Image, ImageDraw
import random

# Texture
img = Image.new('RGB', (256, 256), color=(180, 100, 50))
d = ImageDraw.Draw(img)
for i in range(10000):
    x = random.randint(0, 255)
    y = random.randint(0, 255)
    offset = random.randint(-20, 20)
    d.point((x, y), fill=(180+offset, 100+offset, 50+offset))
img.save('img/tex_p01.jpg')

# Normal Map
norm = Image.new('RGB', (256, 256), color=(128, 128, 255))
norm.save('img/norm_p01.jpg')
print("Generated images")
