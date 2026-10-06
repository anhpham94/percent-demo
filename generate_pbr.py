import sys
from PIL import Image, ImageFilter, ImageOps
import numpy as np

def generate_maps(input_path, output_normal, output_roughness):
    # Load image
    img = Image.open(input_path).convert('RGB')
    
    # 1. Generate Roughness Map (Inverted grayscale + contrast)
    gray = ImageOps.grayscale(img)
    # Roughness: dark areas (creases) should be rougher (white), flat areas should be shinier (darker)
    # Actually for leather, flat areas are often slightly shiny, creases are matte.
    # In Roughness map: White = rough (matte), Black = smooth (shiny).
    # Let's invert grayscale and adjust levels
    roughness = ImageOps.invert(gray)
    
    # Increase contrast for roughness
    # Convert to numpy
    r_arr = np.array(roughness).astype(float)
    r_arr = ((r_arr - r_arr.min()) / (r_arr.max() - r_arr.min())) * 255.0
    # Make it generally quite rough (leather is not glass)
    r_arr = np.clip(r_arr * 0.5 + 128, 0, 255)
    
    roughness_img = Image.fromarray(r_arr.astype(np.uint8))
    roughness_img.save(output_roughness)
    
    # 2. Generate Normal Map (Sobel filter approach)
    # Convert to numpy array of floats
    g_arr = np.array(gray).astype(float) / 255.0
    
    # Sobel kernels
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    from scipy.signal import convolve2d
    dx = convolve2d(g_arr, sobel_x, mode='same', boundary='symm')
    dy = convolve2d(g_arr, sobel_y, mode='same', boundary='symm')
    
    # Normal vector = (-dx, -dy, 1/strength)
    strength = 3.0
    dz = np.ones_like(dx) / strength
    
    length = np.sqrt(dx**2 + dy**2 + dz**2)
    nx = -dx / length
    ny = -dy / length
    nz = dz / length
    
    # Convert to RGB (0-255)
    # X -> R, Y -> G, Z -> B
    n_r = ((nx + 1.0) / 2.0 * 255.0).astype(np.uint8)
    n_g = ((ny + 1.0) / 2.0 * 255.0).astype(np.uint8)
    n_b = ((nz + 1.0) / 2.0 * 255.0).astype(np.uint8)
    
    normal_arr = np.stack([n_r, n_g, n_b], axis=-1)
    normal_img = Image.fromarray(normal_arr)
    normal_img.save(output_normal)

if __name__ == '__main__':
    generate_maps(sys.argv[1], sys.argv[2], sys.argv[3])
