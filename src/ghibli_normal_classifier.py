import logging
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def predict_with_resnet(img_path, resnet_model, log_filename):
    """Generates a WhatsApp-compatible sticker with caption"""
    # Setup logging
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    resnet_img_size = (224, 224)

    """Predicts if an image is 'normal' or 'ghibli' using the loaded ResNet model."""
    try:
        if resnet_model is None:
            return None  # Model not loaded, cannot predict

        img = image.load_img(img_path, target_size=resnet_img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        prediction = resnet_model.predict(img_array)
        print(f"Probabilty of image being normal: {prediction[0][0]}")
        if prediction[0][0] < 0.5:
            return False
        else:
            return True
    except Exception as e:
        logging.error(f"Error during ResNet prediction: {e}")
        return None

if __name__ == "__main__":
    resnet_model = load_model('models\Ghibli-normal-classifier\Resnet_ghibli_normal.h5')
    
    # Path to the image you want to classify
    img_path = r"C:\Users\niksh\Pictures\Kerala\Munnar\Camera360_2015_4_13_012815.jpg"
    result = predict_with_resnet(img_path, resnet_model, log_filename='logs\studio_2025-04-14_04-32-18.log')
    print(f"Need to be converted to Ghibli? {result}")