import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import logging
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def is_normal(img_path, mobilenet_model, log_filename):
    """Generates a WhatsApp-compatible sticker with caption"""
    # Setup logging
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    mobilenet_img_size = (224, 224)

    """Predicts if an image is 'normal' or 'ghibli' using the loaded MobileNet model."""
    try:
        if mobilenet_model is None:
            return None              # Model not loaded, cannot predict

        img = image.load_img(img_path, target_size=mobilenet_img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = mobilenet_model.predict(img_array)
        if prediction[0][0] > 0.5:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error during image classification: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    log_filename = "logs\studio_2025-04-14_05-38-22.log"
    mobilenet_model_path = 'models\Ghibli-normal-classifier\Mobilenet_ghibli_normal.h5'
    
    # Load the model (assuming you have a function to do this)
    try:
        mobilenet_model = load_model(mobilenet_model_path)
        logging.info(f"Classifier model loaded from: {mobilenet_model_path}")
    except Exception as e:
        mobilenet_model = None
        logging.error(f"Error loading Classifier model: {e}. 'Normal' prediction based theming will be skipped.")

    img_path = r"C:\Users\niksh\Desktop\test_01.png"
    is_normal_result = is_normal(img_path, mobilenet_model, log_filename)

    print(f"Is Normal: {is_normal_result}")