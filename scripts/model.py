import os
import logging
from fonts import get_font
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "./stickers"

def generate_sticker(image_path, caption, theme, color, font_name, log_filename):
    """Generates a sticker with caption in the specified font."""
    # Configure logging to use the same file as the Streamlit app
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    logging.info(f"Generating sticker with caption: {caption}, theme: {theme}, color: {color}")

    font_key = font_name.replace("-Regular", "")  # Normalize font name

    # Check if font is available or download it
    font_path = get_font(font_key, log_filename)
    if font_path and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, 40)
        except IOError:
            logging.error(f"Failed to load font {font_name}, using default font.")
            font = ImageFont.load_default()
    else:
        logging.warning(f"Using default font as {font_name} is unavailable.")
        font = ImageFont.load_default()

    # Load Image
    try:
        image = Image.open(image_path)
    except Exception as e:
        logging.error(f"Failed to open image {image_path}: {e}")
        return None

    draw = ImageDraw.Draw(image)

    # Draw caption
    caption_position = (50, 50)
    draw.text(caption_position, caption, fill=color, font=font)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save the file
    output_filename = f"sticker_{caption}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    try:
        image.save(output_path)
        logging.info(f"Sticker successfully saved: {output_path}")
    except Exception as e:
        logging.error(f"Failed to save sticker: {e}")
        return None

    return output_path