from PIL import Image, ImageEnhance

img = Image.open('/Users/tuananhpham/work/shopdongho/percent-3d-customizer/textures/leather_albedo.jpg').convert('L')

# Increase brightness and lower contrast so it serves as a good base for color tinting
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.5)

enhancer2 = ImageEnhance.Contrast(img)
img = enhancer2.enhance(0.5)

img.save('/Users/tuananhpham/work/shopdongho/percent-3d-customizer/textures/leather_grayscale.jpg')
