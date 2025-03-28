import os
import requests
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "stickers"
FONTS_DIR = "fonts"

# Font file mapping
font_files = {
    "Bangers": "Bangers-Regular.ttf",
    "Lobster": "Lobster-Regular.ttf",
    "Pacifico": "Pacifico-Regular.ttf",
    "Fredoka One": "FredokaOne-Regular.ttf",
    "Anton": "Anton-Regular.ttf"
}

# Google Fonts Download Links (Manually fetched)
google_fonts = {
    "Bangers": "https://github.com/google/fonts/raw/main/ofl/bangers/Bangers-Regular.ttf",
    "Lobster": "https://github.com/google/fonts/raw/main/ofl/lobster/Lobster-Regular.ttf",
    "Pacifico": "https://github.com/google/fonts/raw/main/ofl/pacifico/Pacifico-Regular.ttf",
    "Fredoka One": "https://github.com/google/fonts/raw/main/ofl/fredokaone/FredokaOne-Regular.ttf",
    "Anton": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
}

# Ensure fonts directory exists
os.makedirs(FONTS_DIR, exist_ok=True)

# Function to download fonts if missing
def download_font(font_name):
    font_path = os.path.join(FONTS_DIR, font_files[font_name])
    if not os.path.exists(font_path):
        print(f"Downloading {font_name} font...")
        url = google_fonts.get(font_name)
        if url:
            response = requests.get(url)
            with open(font_path, "wb") as f:
                f.write(response.content)
            print(f"{font_name} downloaded and saved.")
        else:
            print(f"No download URL for {font_name}. Please add the font manually.")
    return font_path

def generate_sticker(image_path, text, style, color, font_name):
    # Normalize font name to match dictionary keys
    font_key = font_name.replace("-Regular", "")  # Remove '-Regular' suffix if present

    if font_key not in font_files:
        print(f"Unknown font: {font_name}. Using default font.")
        font = ImageFont.load_default()
    else:
        font_path = download_font(font_key)  # Corrected key lookup
        try:
            font = ImageFont.truetype(font_path, 40)
        except IOError:
            print(f"Failed to load {font_name}, using default font.")
            font = ImageFont.load_default()

    # Load Image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Draw Text
    text_position = (50, 50)
    draw.text(text_position, text, fill=color, font=font)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save the file
    output_filename = f"sticker_{font_key}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    image.save(output_path)

    return output_path  # Ensure correct path is returned