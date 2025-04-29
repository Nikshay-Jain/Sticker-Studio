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
            return None  # Model not loaded, cannot predict

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
    mobilenet_model = load_model('models\Ghibli-normal-classifier\Mobilenet_ghibli_normal.h5')
    
    # Path to the image you want to classify
    img_path = r"C:\Users\niksh\Desktop\test_01.png"
    result = is_normal(img_path, mobilenet_model, log_filename='logs\studio_2025-04-14_04-32-18.log')
    print(f"Ghibli conversion needed: {result}")