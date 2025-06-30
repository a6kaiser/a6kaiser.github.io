#!/usr/bin/env python3
"""
Script to create diagonal friendship flags combining French and Canadian flags.
Preserves original high quality by working with native resolutions.
Creates both 3:2 ratio and Canadian 2:1 ratio versions.
French flag on the left, Canadian flag on the right.
Diagonal goes from top-left to bottom-right.
"""

from PIL import Image, ImageDraw, ImageFilter
import os

def create_friendship_flags():
    # File paths
    french_flag_path = "ignore/Flag_of_France.svg.webp"
    canadian_flag_path = "ignore/Flag_of_Canada_(Pantone).svg.png"
    output_path_32 = "icons/friendship_flag.png"
    output_path_21 = "icons/friendship_flag_canadian_ratio.png"
    
    # Check if input files exist
    if not os.path.exists(french_flag_path):
        print(f"Error: French flag file not found at {french_flag_path}")
        return
    
    if not os.path.exists(canadian_flag_path):
        print(f"Error: Canadian flag file not found at {canadian_flag_path}")
        return
    
    # Load the images at their native high resolution
    print("Loading flag images at native resolution...")
    french_flag = Image.open(french_flag_path).convert('RGBA')
    canadian_flag = Image.open(canadian_flag_path).convert('RGBA')
    
    print(f"French flag native dimensions: {french_flag.size}")
    print(f"Canadian flag native dimensions: {canadian_flag.size}")
    
    # Use the highest resolution as our working resolution to preserve maximum quality
    max_width = max(french_flag.width, canadian_flag.width)
    max_height = max(french_flag.height, canadian_flag.height)
    
    # Scale up to even higher resolution for ultra-smooth processing
    working_width = max_width * 2
    working_height = max_height * 2
    
    print(f"Working at ultra-high resolution: {working_width}x{working_height}")
    
    # Resize both flags to the ultra-high working resolution
    french_flag_hires = french_flag.resize((working_width, working_height), Image.Resampling.LANCZOS)
    canadian_flag_hires = canadian_flag.resize((working_width, working_height), Image.Resampling.LANCZOS)
    
    # Create both versions
    create_flag_version(french_flag_hires, canadian_flag_hires, output_path_32, "3:2 Standard", 300, 200, working_width, working_height)
    create_flag_version(french_flag_hires, canadian_flag_hires, output_path_21, "2:1 Canadian", 300, 150, working_width, working_height)

def create_flag_version(french_flag_hires, canadian_flag_hires, output_path, version_name, final_width, final_height, working_width, working_height):
    print(f"\n=== Creating {version_name} ratio version ===")
    
    # Calculate working dimensions that maintain the target aspect ratio
    target_ratio = final_width / final_height
    if working_width / working_height > target_ratio:
        # Working area is wider than target, constrain by height
        work_height = working_height
        work_width = int(work_height * target_ratio)
    else:
        # Working area is taller than target, constrain by width
        work_width = working_width
        work_height = int(work_width / target_ratio)
    
    print(f"Working dimensions for {version_name}: {work_width}x{work_height}")
    
    # Crop the center portion of both flags to our working dimensions
    french_cropped = crop_center(french_flag_hires, work_width, work_height)
    canadian_cropped = crop_center(canadian_flag_hires, work_width, work_height)
    
    # Create ultra-high-quality mask for the diagonal split
    mask = Image.new('L', (work_width, work_height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw the diagonal split - left triangle for French flag
    diagonal_points = [
        (0, 0),              # top-left
        (0, work_height),    # bottom-left
        (work_width, work_height)  # bottom-right
    ]
    draw.polygon(diagonal_points, fill=255)
    
    # Create super-smooth anti-aliasing with multiple blur passes
    # Use progressive blurring for ultra-smooth edges
    mask = mask.filter(ImageFilter.GaussianBlur(radius=8))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=4))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=2))
    
    print("Applying high-quality diagonal mask...")
    
    # Apply masks with perfect compositing
    french_masked = Image.composite(french_cropped, Image.new('RGBA', (work_width, work_height), (0, 0, 0, 0)), mask)
    
    # Create precise inverse mask
    mask_inverse = Image.new('L', (work_width, work_height), 255)
    draw_inverse = ImageDraw.Draw(mask_inverse)
    draw_inverse.polygon(diagonal_points, fill=0)
    
    # Apply same progressive blurring to inverse mask
    mask_inverse = mask_inverse.filter(ImageFilter.GaussianBlur(radius=8))
    mask_inverse = mask_inverse.filter(ImageFilter.GaussianBlur(radius=4))
    mask_inverse = mask_inverse.filter(ImageFilter.GaussianBlur(radius=2))
    
    canadian_masked = Image.composite(canadian_cropped, Image.new('RGBA', (work_width, work_height), (0, 0, 0, 0)), mask_inverse)
    
    # Combine the masked images
    final_image = Image.alpha_composite(Image.new('RGBA', (work_width, work_height), (255, 255, 255, 255)), canadian_masked)
    final_image = Image.alpha_composite(final_image, french_masked)
    
    # Only now scale down to final size with maximum quality preservation
    print(f"Scaling down to final size {final_width}x{final_height} with quality preservation...")
    final_image = final_image.resize((final_width, final_height), Image.Resampling.LANCZOS)
    
    # Apply subtle sharpening to restore crisp edges after scaling
    final_image = final_image.filter(ImageFilter.UnsharpMask(radius=0.3, percent=120, threshold=1))
    
    # Create icons directory if it doesn't exist
    os.makedirs('icons', exist_ok=True)
    
    # Save with maximum quality
    final_image.save(output_path, 'PNG', optimize=False, compress_level=0)
    print(f"Ultra-high-quality {version_name} friendship flag created: {output_path}")
    print(f"Final dimensions: {final_image.size}")

def crop_center(image, target_width, target_height):
    """Crop the center portion of an image to target dimensions"""
    width, height = image.size
    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    return image.crop((left, top, right, bottom))

if __name__ == "__main__":
    create_friendship_flags() 