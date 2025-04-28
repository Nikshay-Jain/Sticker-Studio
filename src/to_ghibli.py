from datetime import datetime
import os, json, logging, requests, configparser

def generate_ghibli_from_text(text, log_filename=None):
    """
    Generates a Ghibli-style image using the Modelslab API,
    downloads the image, saves it locally, and returns the local file path.

    Args:
        api_key: The API key for the Modelslab API.
        text: The prompt for the image generation.
        log_filename: Optional filename for logging.

    Returns:
        str: The local file path of the saved Ghibli-style image,
             or None if an error occurred.
    """
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        logger = logging.getLogger(__name__)
        
    else:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    url = "https://modelslab.com/api/v6/realtime/text2img"
    ghibli = "Draw in the beutiful, handpainted style of Studio Ghibli. Lush environments, soft lighting, characterfule designs."
    prompt = ghibli + text

    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        api_key = config['modelslab']['api_key']
    except KeyError:
        print("Error: API key not found in config.ini under the [modelslab] section with key 'api_key'.")
    except FileNotFoundError:
        print("Error: config.ini file not found. Please create one in the same directory as the script.")
    except Exception as e:
        print(f"An error occurred while reading the config file: {e}")

    payload = {
        "key": api_key,
        "prompt": prompt,
        "negative_prompt": "blurry, low quality",
        "width": "512",
        "height": "512",
        "samples": "3"
    }

    headers = {
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"Sending request to Modelslab API with prompt: '{prompt}'")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        logger.info("Modelslab API request successful.")

        data = response.json()
        if data.get('output'):
            image_url = data['output'][0]
            logger.info(f"Generated Image URL: {image_url}")

            # Download and save the image
            GHIBLI_DIR = "ghibli images"
            os.makedirs(GHIBLI_DIR, exist_ok=True)
            logger.info(f"Creating directory for images: {GHIBLI_DIR}")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"ghibli_image_{timestamp}.png"
            save_path = os.path.join(GHIBLI_DIR, filename)
            logger.info(f"Saving image to: {save_path}")

            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status()
            logger.info("Image download successful.")

            with open(save_path, 'wb') as f:
                for chunk in image_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Image saved successfully to: {save_path}")
            return save_path
        else:
            logger.warning("Image URL not found in the response.")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        if response is not None:
            logger.error(f"Status code: {response.status_code}")
            logger.error(f"Response text: {response.text}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None

def generate_ghibli_from_image(image_path, log_filename=None):
    ghibli_image_path = image_path
    return ghibli_image_path

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    text_prompt = """Image described: A young man, approximately 20 years old, of South Asian ethnicity, is the focus. He's around 5'8", with a lean build and an oval facial structure. His medium brown skin is complemented by dark, slightly curly hair styled upwards.  His dark brown eyes widen slightly in a focused expression as he eats. He wears a black and white horizontally striped cotton polo shirt, seemingly casual. His hands hold a fork, bringing food to his mouth; his posture is slightly hunched forward, facing the camera at a 45° angle.  He appears engrossed in his meal, conveying a sense of enjoyment.

The background is a dimly lit restaurant booth.  Dark brown leather seating contrasts with beige textured wall paneling. A dark wooden table holds a large, sizzling stone plate filled with a colorful mix of meat, vegetables (peas, green beans, spinach), and fried items. Warm, soft lighting accentuates the steam rising from the food. The overall mood is intimate and warm. The image style is photorealistic, with a slightly soft focus, and has a high resolution feel. There are no text overlays or visual effects."""
    print("Generating Ghibli image...")
    saved_image_path = generate_ghibli_from_text(text_prompt)
    if saved_image_path:
        print(f"The saved Ghibli image path is: {saved_image_path}")