#!/usr/bin/env python3
"""
Create placeholder icons for CloudPad browser extension
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple gamepad icon"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (137, 180, 250, 255)  # Catppuccin blue
    fg_color = (30, 30, 46, 255)     # Dark text

    # Draw rounded rectangle background
    padding = size // 8
    draw.rounded_rectangle(
        [padding, padding, size - padding, size - padding],
        radius=size // 6,
        fill=bg_color
    )

    # Draw simple gamepad D-pad representation
    center_x, center_y = size // 2, size // 2
    d_pad_size = size // 5

    # D-pad cross
    draw.rectangle(
        [center_x - d_pad_size//2, center_y - d_pad_size*1.5,
         center_x + d_pad_size//2, center_y + d_pad_size*1.5],
        fill=fg_color
    )
    draw.rectangle(
        [center_x - d_pad_size*1.5, center_y - d_pad_size//2,
         center_x + d_pad_size*1.5, center_y + d_pad_size//2],
        fill=fg_color
    )

    # Buttons (two circles on the right)
    button_radius = size // 10
    button_offset = size // 4
    draw.ellipse(
        [size - button_offset - button_radius*2, center_y - button_radius - button_offset//2,
         size - button_offset, center_y + button_radius - button_offset//2],
        fill=fg_color
    )
    draw.ellipse(
        [size - button_offset - button_radius*2 - button_offset//2, center_y - button_radius + button_offset//2,
         size - button_offset - button_offset//2, center_y + button_radius + button_offset//2],
        fill=fg_color
    )

    img.save(output_path, 'PNG')
    print(f"Created {output_path}")

def main():
    extension_dir = os.path.join(os.path.dirname(__file__), 'extension')

    # Create icons
    create_icon(16, os.path.join(extension_dir, 'icon16.png'))
    create_icon(48, os.path.join(extension_dir, 'icon48.png'))
    create_icon(128, os.path.join(extension_dir, 'icon128.png'))

    print("All icons created successfully!")

if __name__ == "__main__":
    main()
