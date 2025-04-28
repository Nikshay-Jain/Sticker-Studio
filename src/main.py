# import os, atexit, logging
# from datetime import datetime
# from tensorflow.keras.models import load_model

# from to_ghibli import *
# from segmentor_model import segmentor
# from sticker_generator import conv_to_sticker
# from check_conv_ghibli import is_normal

# UPLOAD_DIR = "uploads"
# OUTPUT_DIR = "stickers"
# FONTS_DIR = "fonts"
# LOG_DIR = "logs"

# _exit_logged = False

# def setup_environment():
#     os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#     os.makedirs(UPLOAD_DIR, exist_ok=True)
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     os.makedirs(FONTS_DIR, exist_ok=True)
#     os.makedirs(LOG_DIR, exist_ok=True)

# def setup_logging():
#     global _exit_logged
#     log_filename = os.path.join(LOG_DIR, f"studio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
#     logging.basicConfig(
#         filename=log_filename,
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )
#     logging.info("=== AI Sticker Studio started ===")
#     atexit.register(log_exit)
#     return log_filename

# def log_exit():
#     global _exit_logged
#     if not _exit_logged:
#         logging.info("=== AI Sticker Studio closed ===")
#         _exit_logged = True

# def load_classifier_model():
#     try:
#         classifier_path = 'models\Ghibli-normal-classifier\Mobilenet_ghibli_normal.h5'
#         model = load_model(classifier_path)
#         logging.info(f"Classifier model loaded from: {classifier_path}")
#         return model
#     except FileNotFoundError:
#         logging.warning(f"Classifier model not found at: {classifier_path}. 'Normal' prediction based theming will be skipped.")
#         return None
#     except Exception as e:
#         logging.error(f"Error loading classifier model: {e}")
#         return None

# def process_sticker(uploaded_file, text_input, color, selected_font, font_files, classifier, log_filename):
#     try:
#         # Save uploaded image
#         file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         logging.info(f"Uploaded file saved: {file_path}")

#         font_filename = font_files[selected_font]

#         # Check if needs theme conversion
#         img_status = is_normal(file_path, classifier, log_filename)
#         if classifier is not None and img_status:
#             logging.info("Applying Ghibli theme...")
#             themed_img_path = os.path.join(OUTPUT_DIR, f"themed_{uploaded_file.name}")
#             if not os.path.exists(themed_img_path):
#                 themed_img_path = generate_ghibli_from_image(file_path, log_filename)
#             else:
#                 logging.info(f"Theme already applied: {themed_img_path}")
#         else:
#             themed_img_path = file_path

#         # Segment and stickerize
#         seg_img_path = segmentor(themed_img_path, log_filename)
#         output_path = conv_to_sticker(seg_img_path, text_input, color, font_filename, log_filename)

#         if os.path.exists(output_path):
#             logging.info(f"Sticker successfully generated: {output_path}")
#             return output_path
#         else:
#             logging.error("Sticker generation failed.")
#             return None
#     except Exception as e:
#         logging.exception(f"Error in processing sticker: {e}")
#         return None

# main.py
import os, atexit, logging
from datetime import datetime
from tensorflow.keras.models import load_model
from PIL import Image # Import Image from PIL for image handling

# Import necessary functions, including the one for text-to-image generation
# Ensure generate_ghibli_from_text exists in your to_ghibli.py file
from to_ghibli import generate_ghibli_from_image, generate_ghibli_from_text
from segmentor_model import segmentor
from sticker_generator import conv_to_sticker
from check_conv_ghibli import is_normal

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "stickers"
FONTS_DIR = "fonts"
LOG_DIR = "logs"
GENERATED_IMG_DIR = "generated_images" # New directory to store images generated from text

_exit_logged = False

# Setup environment (remains the same, added creation of GENERATED_IMG_DIR)
def setup_environment():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FONTS_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(GENERATED_IMG_DIR, exist_ok=True) # Create the new directory for generated images


# Setup logging (remains the same)
def setup_logging():
    global _exit_logged
    log_filename = os.path.join(LOG_DIR, f"studio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("=== AI Sticker Studio started ===")
    atexit.register(log_exit)
    return log_filename

# Log exit (remains the same)
def log_exit():
    global _exit_logged
    if not _exit_logged:
        logging.info("=== AI Sticker Studio closed ===")
        _exit_logged = True

# Load classifier model (remains the same)
def load_classifier_model():
    try:
        # Update the path if your model is located elsewhere
        classifier_path = 'models/Ghibli-normal-classifier/Mobilenet_ghibli_normal.h5'
        model = load_model(classifier_path)
        logging.info(f"Classifier model loaded from: {classifier_path}")
        return model
    except FileNotFoundError:
        logging.warning(f"Classifier model not found at: {classifier_path}. 'Normal' prediction based theming will be skipped.")
        return None
    except Exception as e:
        logging.error(f"Error loading classifier model: {e}")
        return None

# --- New function to process sticker from an uploaded image ---
def process_sticker_from_image(uploaded_file, text_input, color, selected_font, font_files, classifier, log_filename):
    """
    Processes an uploaded image to generate a sticker.
    Includes optional Ghibli theme conversion based on a classifier.
    """
    try:
        # Save uploaded image
        # Using a more robust filename to avoid clashes
        file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logging.info(f"Uploaded file saved: {file_path}")

        font_filename = font_files[selected_font]

        # Check if needs theme conversion using the classifier
        # is_normal function should return True if the image is 'normal' and needs conversion
        img_status = is_normal(file_path, classifier, log_filename)
        if classifier is not None and img_status:
            logging.info("Applying Ghibli theme to uploaded image...")
            # Generate themed image using the imported function
            # generate_ghibli_from_image should save the themed image and return its path
            themed_img_path = generate_ghibli_from_image(file_path, log_filename)
            if not os.path.exists(themed_img_path):
                 logging.error("Ghibli theme conversion failed for uploaded image.")
                 # Decide how to handle failure: either return None or proceed with original image
                 # For now, we'll return None to indicate failure
                 return None
        else:
            # Use the original uploaded image if no theme conversion is needed or classifier is not available
            themed_img_path = file_path
            logging.info("Skipping Ghibli theme conversion for uploaded image.")


        # Segment the (potentially themed) image
        seg_img_path = segmentor(themed_img_path, log_filename)
        if not os.path.exists(seg_img_path):
            logging.error("Image segmentation failed.")
            return None

        # Convert the segmented image to a sticker by adding text
        output_path = conv_to_sticker(seg_img_path, text_input, color, font_filename, log_filename)

        if os.path.exists(output_path):
            logging.info(f"Sticker successfully generated from uploaded image: {output_path}")
            return output_path
        else:
            logging.error("Sticker generation failed after segmentation.")
            return None
    except Exception as e:
        logging.exception(f"Error in processing sticker from uploaded image: {e}")
        return None

# --- New function to process sticker from text input (generates image first) ---
def process_sticker_from_text(text_for_image, text_input, color, selected_font, font_files, classifier, log_filename):
    """
    Generates an image from text input, then processes it to create a sticker.
    Assumes the generated image is already in a desired style (e.g., Ghibli).
    """
    try:
        logging.info(f"Generating image from text: '{text_for_image}'")
        # Generate image from text using the imported function
        # generate_ghibli_from_text should save the image to GENERATED_IMG_DIR and return its path
        generated_img_path = generate_ghibli_from_text(text_for_image, GENERATED_IMG_DIR, log_filename)

        if not os.path.exists(generated_img_path):
            logging.error("Image generation from text failed.")
            return None

        logging.info(f"Image successfully generated from text: {generated_img_path}")

        font_filename = font_files[selected_font]

        # For images generated from text, we can often assume they are already in the desired style,
        # so we might skip the is_normal check and direct theme conversion step that was for uploaded images.
        # If your generate_ghibli_from_text function sometimes produces non-ghibli images or you want
        # to apply further styling, you could add a check/conversion here.
        # For now, we'll use the generated image directly for segmentation.
        themed_img_path = generated_img_path
        logging.info("Using generated image directly for segmentation.")

        # Segment the generated image
        seg_img_path = segmentor(themed_img_path, log_filename)
        if not os.path.exists(seg_img_path):
            logging.error("Image segmentation failed after text-to-image generation.")
            # Clean up the generated image if segmentation fails? (Optional)
            # os.remove(generated_img_path)
            return None

        # Convert the segmented image to a sticker by adding text
        output_path = conv_to_sticker(seg_img_path, text_input, color, font_filename, log_filename)

        if os.path.exists(output_path):
            logging.info(f"Sticker successfully generated from text-based image: {output_path}")
            # Clean up the generated and segmented images after successful sticker creation? (Optional)
            # os.remove(generated_img_path)
            # os.remove(seg_img_path)
            return output_path
        else:
            logging.error("Sticker generation failed after segmentation (from text-based image).")
            return None
    except Exception as e:
        logging.exception(f"Error in processing sticker from text input: {e}")
        return None
