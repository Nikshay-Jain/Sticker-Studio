from datetime import datetime
import os, io, logging, piexif

from PIL import Image, ImageDraw, ImageFont
from fonts import get_font

# Configuration
OUTPUT_DIR = "stickers"
WHATSAPP_MAX_SIZE = (512, 512)
DEFAULT_FONT_SIZE = 40
BACKGROUND_COLOR = (0, 0, 0, 0)  # Transparent

def create_whatsapp_sticker(image, output_path):
    """Final processing to make image WhatsApp-compatible"""
    try:
        # Generate minimal EXIF metadata required for WhatsApp stickers
        exif_dict = {
            "0th": {
                piexif.ImageIFD.Make: "WhatsApp",
                piexif.ImageIFD.Software: "AI Sticker Studio"
            },
            "Exif": {},
            "GPS": {},
            "Interop": {},
            "1st": {},
            "thumbnail": None
        }
        exif_bytes = piexif.dump(exif_dict)

        # Save as WebP first (without EXIF)
        output_io = io.BytesIO()
        image.save(output_io, format="WEBP", lossless=True)  # Lossless WebP for stickers

        # Write WebP to file
        with open(output_path, "wb") as f:
            f.write(output_io.getvalue())

        # Inject EXIF metadata
        piexif.insert(exif_bytes, output_path)
        
        return True
    except Exception as e:
        logging.error(f"Error creating WhatsApp sticker: {e}")
        return False

def conv_to_sticker(seg_img_path, caption, color, font_name, log_filename=None):
    """Generates a WhatsApp-compatible sticker with caption at the TOP"""
    # Setup logging
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    try:
        # 1. Load and validate image
        if not os.path.exists(seg_img_path):
            raise FileNotFoundError(f"Image not found at {seg_img_path}")
            
        image = Image.open(seg_img_path).convert("RGBA")
        
        # 2. Process image to sticker format
        image.thumbnail(WHATSAPP_MAX_SIZE, Image.LANCZOS)
        sticker = Image.new("RGBA", WHATSAPP_MAX_SIZE, BACKGROUND_COLOR)
        x_offset = (WHATSAPP_MAX_SIZE[0] - image.size[0]) // 2
        y_offset = (WHATSAPP_MAX_SIZE[1] - image.size[1]) // 2
        sticker.paste(image, (x_offset, y_offset), image)
        
        # 3. Add caption if provided
        if caption:
            # Get font (with fallback)
            font_path = get_font(font_name.replace("-Regular", ""), log_filename)
            try:
                font = ImageFont.truetype(font_path, DEFAULT_FONT_SIZE) if font_path else ImageFont.load_default()
            except:
                font = ImageFont.load_default()
                logging.warning(f"Using default font - couldn't load {font_name}")
            
            # Calculate text position (centered at TOP)
            draw = ImageDraw.Draw(sticker)
            text_width = draw.textlength(caption, font=font)
            text_position = (
                (WHATSAPP_MAX_SIZE[0] - text_width) // 2,  # Center horizontally
                20  # 20px from top
            )
            
            # Add text with outline for better visibility
            for x_shift in [-1, 0, 1]:
                for y_shift in [-1, 0, 1]:
                    if x_shift or y_shift:
                        draw.text(
                            (text_position[0] + x_shift, text_position[1] + y_shift),
                            caption,
                            fill="black",
                            font=font
                        )
            draw.text(text_position, caption, fill=color, font=font)
        
        # 4. Save as WhatsApp-compatible sticker
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_filename = f"sticker_{caption}_{datetime.now().strftime('%H-%M-%S')}.webp"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        if create_whatsapp_sticker(sticker, output_path):
            logging.info(f"Successfully created sticker: {output_path}")
            return output_path
        
    except Exception as e:
        logging.error(f"Error generating sticker: {e}")
    
    return None

if __name__ == "__main__":
    # Example usage
    image_path = "uploads\Camera360_2015_4_13_013444.jpg"
    caption = "Hello World!"
    color = (255, 0, 0)  # Red
    font_name = "Bangers-Regular"

    # Configuration
    OUTPUT_DIR = "stickers_new"
    WHATSAPP_MAX_SIZE = (512, 512)
    DEFAULT_FONT_SIZE = 40
    BACKGROUND_COLOR = (0, 0, 0, 0)

    sticker_path = conv_to_sticker(image_path, caption, color, font_name)
    if sticker_path:
        print(f"Sticker created at: {sticker_path}")
    else:
        print("Failed to create sticker.")