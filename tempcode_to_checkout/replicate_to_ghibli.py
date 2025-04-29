import os
import logging
import configparser
import replicate
from datetime import datetime
from urllib.request import urlretrieve

# Load API token from config.ini
def load_api_token(config_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get("replicate", "api_token")

# Set up logging
def setup_logger(log_file_path):
    logger = logging.getLogger("ghibli_logger")
    logger.setLevel(logging.INFO)
    # Avoid adding multiple handlers if logger already has handlers
    if not logger.handlers:
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

# Ensure output directory exists
def ensure_output_dir(directory="ghibli_images"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# Function 1: Convert an image to Ghibli style
def convert_image_to_ghibli(image_path, prompt, log_file_path, config_path="config.ini"):
    logger = setup_logger(log_file_path)
    try:
        api_token = load_api_token(config_path)
        replicate_client = replicate.Client(api_token=api_token)
        logger.info(f"Starting image-to-Ghibli conversion for {image_path} with prompt: '{prompt}'")

        # Prepare inputs
        inputs = {
            "prompt": prompt,
            "spatial_img": open(image_path, "rb"),
            "control_type": "Ghibli",
            "lora_scale": 1.0,
            "width": 768,
            "height": 768,
            "seed": 42
        }

        # Run the model
        output = replicate_client.run(
            "adarshnagrikar14/studio-ai:latest",
            input=inputs
        )

        # Save the output image
        output_dir = ensure_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"ghibli_image_{timestamp}.png")
        urlretrieve(output[0], output_path)
        logger.info(f"Image saved to {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Error in convert_image_to_ghibli: {e}")
        raise

# Function 2: Generate a Ghibli-style image from text
def generate_ghibli_from_text(prompt, log_file_path, config_path="config.ini"):
    logger = setup_logger(log_file_path)
    try:
        api_token = load_api_token(config_path)
        replicate_client = replicate.Client(api_token=api_token)
        logger.info(f"Starting text-to-Ghibli generation with prompt: '{prompt}'")

        # Prepare inputs
        inputs = {
            "prompt": prompt,
            "control_type": "Ghibli",
            "lora_scale": 1.0,
            "width": 768,
            "height": 768,
            "seed": 42
        }

        # Run the model
        output = replicate_client.run(
            "adarshnagrikar14/studio-ai:latest",
            input=inputs
        )

        # Save the output image
        output_dir = ensure_output_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"ghibli_text_image_{timestamp}.png")
        urlretrieve(output[0], output_path)
        logger.info(f"Image saved to {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Error in generate_ghibli_from_text: {e}")
        raise

# Manual testing
if __name__ == "__main__":
    # Example usage
    log_file = "ghibli_generation.log"

    # Test convert_image_to_ghibli
    try:
        image_path = "path_to_your_image.jpg"
        prompt = "A peaceful village surrounded by mountains in Studio Ghibli style"
        result_path = convert_image_to_ghibli(image_path, prompt, log_file)
        print(f"Image-to-Ghibli result saved at: {result_path}")
    except Exception as e:
        print(f"Error during image-to-Ghibli conversion: {e}")

    # Test generate_ghibli_from_text
    try:
        prompt = "A magical forest with glowing trees and creatures in Studio Ghibli style"
        result_path = generate_ghibli_from_text(prompt, log_file)
        print(f"Text-to-Ghibli result saved at: {result_path}")
    except Exception as e:
        print(f"Error during text-to-Ghibli generation: {e}")
