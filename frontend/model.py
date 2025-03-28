import os
import requests
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "stickers"
FONTS_DIR = "fonts"

# Font file mapping (local file names)
font_files = {
    "Bangers": "Bangers-Regular.ttf",
    "Lobster": "Lobster-Regular.ttf",
    "Pacifico": "Pacifico-Regular.ttf",
    "Anton": "Anton-Regular.ttf"
}

# Google Fonts Download Links (manually fetched)
google_fonts = {
    "Bangers": "https://github.com/google/fonts/raw/main/ofl/bangers/Bangers-Regular.ttf",
    "Lobster": "https://github.com/google/fonts/raw/main/ofl/lobster/Lobster-Regular.ttf",
    "Pacifico": "https://github.com/google/fonts/raw/main/ofl/pacifico/Pacifico-Regular.ttf",
    "Anton": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
}

# Ensure fonts directory exists
os.makedirs(FONTS_DIR, exist_ok=True)

# Function to download fonts if missing
def download_font(font_name):
    """Checks if a font is available; if not, downloads it."""
    if font_name not in font_files:
        print(f"Font '{font_name}' is not recognized. Using default font.")
        return None

    font_path = os.path.join(FONTS_DIR, font_files[font_name])
    
    if not os.path.exists(font_path):
        print(f"Downloading {font_name} font...")
        url = google_fonts.get(font_name)
        if url:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Raise error for bad responses
                with open(font_path, "wb") as f:
                    f.write(response.content)
                print(f"{font_name} downloaded and saved.")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {font_name}: {e}")
                return None
        else:
            print(f"No download URL for {font_name}. Please add the font manually.")
            return None

    return font_path

def generate_sticker(image_path, text, style, color, font_name):
    """Generates a sticker with text in the specified font."""
    font_key = font_name.replace("-Regular", "")  # Normalize font name

    # Check if font is available or download it
    font_path = download_font(font_key)

    # Load font or fallback to default
    if font_path and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, 40)
        except IOError:
            print(f"Failed to load {font_name}, using default font.")
            font = ImageFont.load_default()
    else:
        print(f"Using default font as {font_name} is unavailable.")
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