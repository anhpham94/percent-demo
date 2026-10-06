from PIL import Image, ImageFilter
import math

def generate_maps(input_path, normal_path, roughness_path):
    img = Image.open(input_path).convert('L') # Convert to grayscale
    width, height = img.size
    
    # Generate Roughness (Invert and adjust contrast)
    roughness = Image.new('L', (width, height))
    for y in range(height):
        for x in range(width):
            val = img.getpixel((x, y))
            # Darker pixels in albedo usually mean deeper crevices -> higher roughness or lower? 
            # In crevices, it might be rougher. Let's just use inverted value with some tweaking
            r_val = int(255 - val * 0.5) 
            roughness.putpixel((x, y), r_val)
    roughness.save(roughness_path)
    
    # Generate Normal Map (Sobel filter approximation)
    normal = Image.new('RGB', (width, height))
    # Simple Sobel
    for y in range(1, height-1):
        for x in range(1, width-1):
            tl = img.getpixel((x-1, y-1))
            tc = img.getpixel((x, y-1))
            tr = img.getpixel((x+1, y-1))
            cl = img.getpixel((x-1, y))
            cr = img.getpixel((x+1, y))
            bl = img.getpixel((x-1, y+1))
            bc = img.getpixel((x, y+1))
            br = img.getpixel((x+1, y+1))
            
            dX = (tr + 2*cr + br) - (tl + 2*cl + bl)
            dY = (bl + 2*bc + br) - (tl + 2*tc + tr)
            
            # Normalize
            # Strength of normal
            strength = 2.0
            dX = dX / 255.0 * strength
            dY = dY / 255.0 * strength
            dZ = 1.0
            
            length = math.sqrt(dX*dX + dY*dY + dZ*dZ)
            nX = dX / length
            nY = dY / length
            nZ = dZ / length
            
            # Convert to RGB [0, 255]
            r = int((nX + 1.0) * 127.5)
            g = int((nY + 1.0) * 127.5)
            b = int((nZ + 1.0) * 127.5)
            
            normal.putpixel((x, y), (r, g, b))
            
    # Edge handling - just copy from neighbors for simplicity
    for x in range(width):
        normal.putpixel((x, 0), normal.getpixel((x, 1)))
        normal.putpixel((x, height-1), normal.getpixel((x, height-2)))
    for y in range(height):
        normal.putpixel((0, y), normal.getpixel((1, y)))
        normal.putpixel((width-1, y), normal.getpixel((width-2, y)))
        
    normal.save(normal_path)
    print("Generated Normal and Roughness maps.")

generate_maps(
    '/Users/tuananhpham/.gemini/antigravity-ide/brain/9213cad5-45b6-4ad8-a01b-4828b2c38f34/leather_albedo_1791308679637.jpg',
    '/Users/tuananhpham/work/shopdongho/percent-3d-customizer/textures/leather_normal.jpg',
    '/Users/tuananhpham/work/shopdongho/percent-3d-customizer/textures/leather_roughness.jpg'
)
