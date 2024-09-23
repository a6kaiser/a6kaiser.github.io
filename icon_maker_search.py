from PIL import Image, ImageDraw

# Function to draw a circle with variable thickness
def draw_circle(draw, center, radius, outline, thickness):
    x0, y0 = center
    draw.ellipse(
        [x0 - radius, y0 - radius, x0 + radius, y0 + radius],
        outline=outline, width=thickness
    )

# Function to draw a search icon with a circle and a diagonal line
def make_search_icon(height, width, supersampling_factor, circle_radius, circle_thickness, circle_center, handle_length, handle_thickness, handle_angle, color):
    # Create a high-resolution transparent image
    large_height = height * supersampling_factor
    large_width = width * supersampling_factor
    image = Image.new("RGBA", (large_width, large_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw the circle (magnifying glass lens)
    scaled_radius = circle_radius * supersampling_factor
    scaled_thickness = circle_thickness * supersampling_factor
    scaled_center = (circle_center[0] * supersampling_factor, circle_center[1] * supersampling_factor)

    draw_circle(draw, scaled_center, scaled_radius, outline=color, thickness=scaled_thickness)

    # Draw the diagonal handle
    # Calculate the starting point of the line (from the circle edge)
    handle_start_x = scaled_center[0] + scaled_radius * (2**0.5 / 2)  # 45-degree angle from circle center
    handle_start_y = scaled_center[1] + scaled_radius * (2**0.5 / 2)

    # Calculate the endpoint of the handle
    handle_length_scaled = handle_length * supersampling_factor
    handle_end_x = handle_start_x + handle_length_scaled * (2**0.5 / 2)
    handle_end_y = handle_start_y + handle_length_scaled * (2**0.5 / 2)

    draw.line(
        [(handle_start_x, handle_start_y), (handle_end_x, handle_end_y)],
        fill=color, width=handle_thickness * supersampling_factor
    )

    # Downscale the image to the desired display size with anti-aliasing
    icon = image.resize((width, height), Image.ANTIALIAS)

    # Save the downscaled image with a transparent background
    icon.save(f"icons/search_icon.png")

# Variables for icon dimensions and design
height = 160  # Final display height
width = 160   # Final display width
supersampling_factor = 4  # Increase resolution by this factor for better quality
circle_radius = 40  # Radius of the circle
circle_thickness = 16  # Thickness of the circle border
circle_center = (80, 80)  # Center of the circle (middle of the icon)
handle_length = 60  # Length of the diagonal handle
handle_thickness = 16  # Thickness of the handle
handle_angle = 45  # Angle of the diagonal handle (in degrees)
color = "black"  # Icon color

# Create the search icon
make_search_icon(height, width, supersampling_factor, circle_radius, circle_thickness, circle_center, handle_length, handle_thickness, handle_angle, color)
