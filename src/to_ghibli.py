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

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    text_prompt = """Image described: A young man, approximately 20 years old, of South Asian ethnicity, is the focus. He's around 5'8", with a lean build and an oval facial structure. His medium brown skin is complemented by dark, slightly curly hair styled upwards.  His dark brown eyes widen slightly in a focused expression as he eats. He wears a black and white horizontally striped cotton polo shirt, seemingly casual. His hands hold a fork, bringing food to his mouth; his posture is slightly hunched forward, facing the camera at a 45° angle.  He appears engrossed in his meal, conveying a sense of enjoyment.

The background is a dimly lit restaurant booth.  Dark brown leather seating contrasts with beige textured wall paneling. A dark wooden table holds a large, sizzling stone plate filled with a colorful mix of meat, vegetables (peas, green beans, spinach), and fried items. Warm, soft lighting accentuates the steam rising from the food. The overall mood is intimate and warm. The image style is photorealistic, with a slightly soft focus, and has a high resolution feel. There are no text overlays or visual effects."""
    print("Generating Ghibli image...")
    saved_image_path = generate_ghibli_from_text(text_prompt)
    if saved_image_path:
        print(f"The saved Ghibli image path is: {saved_image_path}")





import PIL.Image
import io, os
import requests
import configparser
import hashlib
import logging

# --- Configuration File Setup ---
CONFIG_FILE = "config.ini"
API_KEY_SECTION = "stability"
API_KEY_OPTION = "api_key"
OUTPUT_DIR = "ghibli images"

# We won't use basicConfig here initially, as we want to configure
# logging *within* the function based on the provided file path.
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# Get a logger for this module.
logger = logging.getLogger(__name__)
# Prevent propagation to the root logger which might have handlers
# added elsewhere (like if basicConfig was called before this script runs).
# This gives us finer control.
logger.propagate = False


def load_config(filename=CONFIG_FILE):
    """
    Loads configuration from the specified INI file.

    Returns:
        A ConfigParser object if successful, None otherwise.
    """
    config = configparser.ConfigParser()
    try:
        read_files = config.read(filename)
        if not read_files:
            # Keeping these fundamental config errors as prints for immediate user visibility.
            print(f"Error: Configuration file '{filename}' not found or is empty.")
            print("Please create a config.ini file with a '[stability]' section and an 'api_key'.")
            return None
        return config
    except Exception as e:
        print(f"Error reading configuration file '{filename}': {e}")
        return None

def get_stability_key(config):
    """
    Extracts the Stability AI key from the loaded configuration.

    Args:
        config: A ConfigParser object loaded from the config file.

    Returns:
        The API key string if found, None otherwise.
    """
    try:
        key = config.get(API_KEY_SECTION, API_KEY_OPTION)
        if not key:
            print(f"Error: '{API_KEY_OPTION}' in section '[{API_KEY_SECTION}]' in '{CONFIG_FILE}' is empty.")
            print("Please provide your actual Stability AI key.")
            return None
        return key
    except (configparser.NoSectionError, configparser.NoOptionError):
        print(f"Whoops! Looks like your '{CONFIG_FILE}' is missing the '[{API_KEY_SECTION}]' section or the '{API_KEY_OPTION}' inside it.")
        print(f"Please make sure your config.ini looks like this:")
        print(f"[{API_KEY_SECTION}]")
        print(f"{API_KEY_OPTION} = YOUR_STABILITY_AI_KEY_HERE")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the key from config: {e}")
        return None


def save_ghibli_image(image, identifier, directory=OUTPUT_DIR):
    """
    Saves the image to the specified directory with a hashed filename.

    Args:
        image: A PIL.Image.Image object to save.
        identifier: A string used to generate a unique filename hash (e.g., the prompt).
        directory: The directory path to save the image in.

    Returns:
        The full path to the saved image file if successful, None otherwise.
    """
    try:
        os.makedirs(directory, exist_ok=True)

        hash_object = hashlib.sha256(identifier.encode('utf-8'))
        hex_dig = hash_object.hexdigest()

        filename = f"{hex_dig}.png"
        filepath = os.path.join(directory, filename)

        image.save(filepath)
        return filepath

    except Exception as e:
        # This error is part of the save logic, maybe log it later if we unify logging setup.
        print(f"Error saving image to '{directory}': {e}")
        return None


# --- The single entry point function (now with logging file path!) ---
def generate_and_save_ghibli_image(description, log_filepath=None): # <-- Added log_filepath
    """
    Generates a Ghibli-style image based on a description using Stability AI,
    saves it to a file with a hashed filename, and returns the saved file path.

    Optionally logs output to a specified file.

    Args:
        description: The text description for the image content.
        log_filepath: Optional. The path to a file where logging output should be written.
                      If None, logs will go to the console (if configured elsewhere)
                      or just disappear into the void if no handlers are set.

    Returns:
        The absolute path to the saved image file, or None if generation or saving failed.
    """
    # --- Configure Logging for this specific run ---
    # This part ensures logs go to the specified file (and maybe console)
    # regardless of any prior logging setup (like basicConfig).

    # Clear existing handlers from this logger to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the logging level for this logger
    logger.setLevel(logging.INFO)

    # Define a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Add a console handler so we still see messages in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Set level for console output
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # If a log file path is provided, add a file handler
    if log_filepath:
        try:
            file_handler = logging.FileHandler(log_filepath)
            file_handler.setLevel(logging.INFO) # Set level for file output
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"Logging output directed to file: {log_filepath}")
        except Exception as e:
            # Log this error to the console handler we already set up
            logger.error(f"Failed to set up file logging to {log_filepath}: {e}")
            # The function will continue, but logs will only go to the console


    logger.info(f"Attempting to generate Ghibli image for description: '{description}'")

    # 1. Load configuration and get the API key
    config = load_config()
    if config is None:
        logger.error("Setup failed: Could not load configuration.")
        # Note: load_config and get_stability_key still use print for
        # their specific config-related failures, which might appear
        # before the logging setup in this function completes if called
        # directly outside of this function. For calls *within* this
        # function, the prints from load_config/get_stability_key
        # might appear alongside the logs configured here.
        return None

    stability_key = get_stability_key(config)
    if stability_key is None:
        logger.error("Setup failed: Could not retrieve Stability AI key.")
        return None

    # --- Setup for Stability AI API Call ---
    STABILITY_REST_API_URL = "https://api.stability.ai"
    STABILITY_GENERATE_ENDPOINT = "/v2beta/stable-image/generate/ultra"

    # 2. Prepare the full prompt (including the Ghibli style prefix)
    prompt_text = f"Hand-painted illustration in the style of Studio Ghibli. monotonic white background color, soft light, naturalistic details. {description}"
    logger.info(f"Using full prompt: '{prompt_text[:150]}...'")

    api_url = f"{STABILITY_REST_API_URL}{STABILITY_GENERATE_ENDPOINT}"

    headers = {
        "Authorization": f"Bearer {stability_key}",
        "Accept": "image/*"
    }

    files = [
        ("prompt", (None, prompt_text)),
        ("output_format", (None, "png")),
        ("aspect_ratio", (None, "1:1")),
        ("width", (None, "512")),
        ("height", (None, "512"))
    ]

    # 3. Call the Stability AI API
    logger.info("Sending request to Stability AI...")
    try:
        response = requests.post(api_url, headers=headers, files=files)

        # 4. Handle the API response
        if response.status_code == 200:
            logger.info("Stability AI API call successful.")
            img_data = response.content
            try:
                img = PIL.Image.open(io.BytesIO(img_data))
                logger.info("Image data received and opened successfully.")

                # 5. Save the generated image
                logger.info(f"Saving image to directory '{OUTPUT_DIR}'...")
                saved_path = save_ghibli_image(img, prompt_text)

                if saved_path:
                    logger.info(f"Process complete. Image saved to: {saved_path}")
                    return saved_path # Return the path on success
                else:
                    logger.error("Image generation successful, but saving failed.")
                    return None # Generation worked, but saving didn't

            except PIL.UnidentifiedImageError:
                logger.error("API returned 200 OK, but the data was not a recognizable image format.")
                logger.error(f"Response body snippet (might be large): {response.content[:500]}...")
                return None
            except Exception as e:
                logger.error(f"An unexpected error occurred during image processing (opening): {e}")
                return None

        else:
            logger.error(f"Stability AI API call failed. Status code: {response.status_code}")
            logger.error(f"Response body: {response.text}")
            return None # API call failed

    except requests.exceptions.RequestException as e:
        logger.error(f"Network or request error during Stability AI API call: {e}")
        return None # Request failed
    except Exception as e:
        logger.error(f"An unexpected error occurred during the overall generation process: {e}")
        return None # Any other unexpected error
    finally:
        # --- Clean up handlers ---
        # It's often good practice to clean up handlers added dynamically,
        # especially if this function might be called multiple times
        # with different logging configurations or if the handlers
        # consume resources.
        if logger.hasHandlers():
             for handler in logger.handlers:
                 handler.close() # Close the handler's resources (like file handles)
             logger.handlers.clear() # Remove handlers from the logger
