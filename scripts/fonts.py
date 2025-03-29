import os
import logging
import requests

FONTS_DIR = "./fonts"

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

# Function to download fonts if missing
def get_font(font_name, log_filename):
    # Configure logging to append logs to the latest file
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
    """Checks if a font is available; if not, downloads it."""
    if font_name not in font_files:
        logging.warning(f"Font '{font_name}' is not recognized. Using default font.")
        return None

    font_path = os.path.join(FONTS_DIR, font_files[font_name])
    
    if not os.path.exists(font_path):
        logging.info(f"Downloading {font_name} font...")

        url = google_fonts.get(font_name)
        if url:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()                # Raise error for bad responses
                with open(font_path, "wb") as f:
                    f.write(response.content)
                logging.info(f"{font_name} downloaded and saved at {font_path}.")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error downloading {font_name}: {e}")
                return None
        else:
            logging.error(f"No download URL found for {font_name}. Please add the font manually.")
            return None

    return font_path