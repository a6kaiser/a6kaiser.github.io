from PIL import Image, ImageDraw

# Function to draw rounded rectangle with proper corner alignment
def draw_rounded_rect(draw, xy, radius, outline, thickness, fill=None):
    x0, y0, x1, y1 = xy
    # Draw corner arcs
    draw.arc([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=outline, width=thickness)  # Top-left
    draw.arc([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=outline, width=thickness)  # Top-right
    draw.arc([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=outline, width=thickness)     # Bottom-right
    draw.arc([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=outline, width=thickness)   # Bottom-left

    # Draw straight sides
    draw.line([(x0 + radius, y0+thickness//2-1), (x1 - radius, y0+thickness//2-1)], fill=outline, width=thickness)  # Top
    draw.line([(x0 + radius, y1-thickness//2+1), (x1 - radius, y1-thickness//2+1)], fill=outline, width=thickness)  # Bottom
    draw.line([(x0+thickness//2-1, y0 + radius), (x0+thickness//2-1, y1 - radius)], fill=outline, width=thickness)  # Left
    draw.line([(x1-thickness//2+1, y0 + radius), (x1-thickness//2+1, y1 - radius)], fill=outline, width=thickness)  # Right

    # Optionally fill inside the square
    if fill:
        draw.rectangle([x0 + thickness // 2, y0 + thickness // 2, x1 - thickness // 2, y1 - thickness // 2], outline=None, fill=fill)

def make_icon(height,width,supersampling_factor,square_margin,radius,color,border_thickness,vertical_bar_x,arrow_base_x,arrow_size,case):
    # Create a high-resolution transparent image
    large_height = height * supersampling_factor  # High-resolution canvas size (600x600)
    large_width = width * supersampling_factor
    image = Image.new("RGBA", (large_width,large_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw the rounded square
    draw_rounded_rect(
        draw,
        [square_margin, square_margin, large_width - square_margin, large_height - square_margin],
        radius,
        color,
        border_thickness
    )

    # Draw the vertical line flush with the square's outer edge
    draw.line(
        [(vertical_bar_x, square_margin), (vertical_bar_x, large_height - square_margin)],
        fill=color, width=border_thickness
    )

    # Draw a right-angled arrow tip centered vertically at arrow_base_x, flipped 180 degrees
    half_arrow_height = abs(arrow_size) // 2
    draw.polygon(
        [
            (arrow_base_x, large_height // 2 - half_arrow_height),  # Top point of the base
            (arrow_base_x, large_height // 2 + half_arrow_height),  # Bottom point of the base
            (arrow_base_x - arrow_size, large_height // 2)          # Tip of the arrow (to the left now)
        ],
        fill=color
    )

    # Downscale the image to the desired display size with anti-aliasing
    icon = image.resize((width, height), Image.ANTIALIAS)

    # Save the downscaled image with a transparent background
    icon.save(f"icons/sidebar_{case}_icon.png")

# Variables for icon dimensions and coordinates
height = 200  # Final display size (200x200 pixels)
width = 250
supersampling_factor = 1  # Increase resolution by this factor for better quality
border_thickness = 20 * supersampling_factor  # Border thickness scaled (30)
radius = 40 * supersampling_factor  # Corner radius scaled (120)
square_margin = 4 * supersampling_factor  # Margin from the edge (60)
color = "black"  # Icon color (can be changed)

vertical_bar_x = width * 3/8 * supersampling_factor # Close:80 Open:120
arrow_base_x = width * 7/10 * supersampling_factor # Close:130 Open:70
arrow_size = width * 4/20 * supersampling_factor  # Arrow size scaled (90)
make_icon(height,width,supersampling_factor,square_margin,radius,color,border_thickness,vertical_bar_x,arrow_base_x,arrow_size,"close")

vertical_bar_x = width * 5/8 * supersampling_factor # Close:80 Open:120
arrow_base_x = width * 3/10 * supersampling_factor # Close:130 Open:70
arrow_size = -arrow_size  # Arrow size scaled (90)
make_icon(height,width,supersampling_factor,square_margin,radius,color,border_thickness,vertical_bar_x,arrow_base_x,arrow_size,"open")
