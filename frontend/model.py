import os
from PIL import Image, ImageDraw, ImageFont
import uuid

STATIC_DIR = "static"

def generate_sticker(file_path, text, style):
    """Processes the image and adds text, then saves it to the static directory."""
    
    # Open the uploaded image
    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)

    # Add text to image (basic placeholder implementation)
    font = ImageFont.load_default()
    text_position = (10, 10)
    draw.text(text_position, text, fill="red", font=font)

    # Generate a unique filename
    output_filename = f"sticker_{uuid.uuid4().hex}.png"
    output_path = os.path.join(STATIC_DIR, output_filename)
    
    # Save the processed sticker
    image.save(output_path)

    return output_filename  # Return the new filename
