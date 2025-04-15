from datetime import datetime
import os, json, logging, requests, configparser

def generate_ghibli_image(text, log_filename=None):
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
    ghibli = "Create an image in the style of Studio Ghibli of "
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
        "samples": "1"
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
            os.makedirs("ghibli images", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"ghibli_image_{timestamp}.png"
            GHIBLI_DIR = os.makedirs("ghibli images", exist_ok=True)
            logger.info(f"Creating directory for images: ghibli images")
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

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    text_prompt = "a bunny dressed as a tired footballer in a field"
    print("Generating Ghibli image...")
    saved_image_path = generate_ghibli_image(text_prompt)
    if saved_image_path:
        print(f"The saved Ghibli image path is: {saved_image_path}")