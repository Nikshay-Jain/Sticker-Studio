import os, atexit, logging
from datetime import datetime
from segmentor_model import segmentor
from to_ghibli_grok_hardcoded import theme_convertor
from text_to_ghibli import generate_ghibli_from_text
from sticker_generator import conv_to_sticker
from check_conv_ghibli import is_normal
from tensorflow.keras.models import load_model

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "stickers"
FONTS_DIR = "fonts"
LOG_DIR = "logs"

_exit_logged = False

def setup_environment():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FONTS_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

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

def log_exit():
    global _exit_logged
    if not _exit_logged:
        logging.info("=== AI Sticker Studio closed ===")
        _exit_logged = True

def load_classifier_model():
    try:
        classifier_path = 'models\Ghibli-normal-classifier\Mobilenet_ghibli_normal.h5'
        model = load_model(classifier_path)
        logging.info(f"Classifier model loaded from: {classifier_path}")
        return model
    except FileNotFoundError:
        logging.warning(f"Classifier model not found at: {classifier_path}. 'Normal' prediction based theming will be skipped.")
        return None
    except Exception as e:
        logging.error(f"Error loading classifier model: {e}")
        return None

def process_sticker(uploaded_file, text_input, color, selected_font, font_files, classifier, log_filename):
    try:
        # Save uploaded image
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logging.info(f"Uploaded file saved: {file_path}")

        font_filename = font_files[selected_font]

        # Check if needs theme conversion
        img_status = is_normal(file_path, classifier, log_filename)
        if classifier is not None and img_status:
            logging.info("Applying Ghibli theme...")
            themed_img_path = os.path.join(OUTPUT_DIR, f"themed_{uploaded_file.name}")
            if not os.path.exists(themed_img_path):
                themed_img_path = theme_convertor(file_path, log_filename)
            else:
                logging.info(f"Theme already applied: {themed_img_path}")
        else:
            themed_img_path = file_path

        # Segment and stickerize
        seg_img_path = segmentor(themed_img_path, log_filename)
        output_path = conv_to_sticker(seg_img_path, text_input, color, font_filename, log_filename)

        if os.path.exists(output_path):
            logging.info(f"Sticker successfully generated: {output_path}")
            return output_path
        else:
            logging.error("Sticker generation failed.")
            return None
    except Exception as e:
        logging.exception(f"Error in processing sticker: {e}")
        return None

def generate_image_from_prompt(prompt, log_filename):
    # your text2img model inference here
    # return generated image path
    pass

def process_uploaded_image_to_sticker(uploaded_file, caption, color, selected_font, is_normal_classifier, log_filename):
    # everything for processing uploaded file to sticker
    # classify -> resize -> caption -> save
    # return final sticker path
    pass