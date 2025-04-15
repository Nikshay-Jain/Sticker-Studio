import os
import sys
import base64
import time
import requests
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def convert_to_ghibli_style(image_path, output_dir, prompt=None):
    """
    Convert an image to Studio Ghibli style using Replicate's API.
    
    Args:
        image_path (str): Path to input image.
        output_dir (str): Directory to save output image.
        prompt (str, optional): Additional prompt to guide the style.
    
    Returns:
        str: Path to saved output image.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the image
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except Exception as e:
        print(f"Error reading input image: {e}")
        return None
    
    # Get API token from environment
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("Error: REPLICATE_API_TOKEN not found in environment variables.")
        return None
    
    # Default prompt if none provided
    if not prompt:
        prompt = "Studio Ghibli style, Hayao Miyazaki art style, anime, hand-drawn, detailed background, soft colors, magical atmosphere"
    
    # Upload the image to a hosting service or your own server to obtain a URL
    # For demonstration, we'll assume you have a function upload_image() that returns the image URL
    image_url = upload_image(image_path)  # You need to implement this function
    
    if not image_url:
        print("Error: Failed to upload image and obtain URL.")
        return None
    
    # Prepare the API request
    api_url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": "your_model_version_id",  # Replace with the actual version ID
        "input": {
            "prompt": prompt,
            "image": image_url
        }
    }
    
    # Make the API request
    print("Converting image to Studio Ghibli style...")
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        prediction = response.json()
        
        # Poll the API to get the result
        prediction_url = prediction["urls"]["get"]
        while True:
            result_response = requests.get(prediction_url, headers=headers)
            result_response.raise_for_status()
            result = result_response.json()
            if result["status"] == "succeeded":
                break
            elif result["status"] == "failed":
                print("Error: Prediction failed.")
                return None
            time.sleep(1)
        
        # Download the output image
        output_image_url = result["output"]
        output_image_response = requests.get(output_image_url)
        output_image_response.raise_for_status()
        
        # Save the output image
        base_filename = os.path.basename(image_path)
        filename_without_ext = os.path.splitext(base_filename)[0]
        output_path = os.path.join(output_dir, f"{filename_without_ext}_ghibli.png")
        with open(output_path, "wb") as f:
            f.write(output_image_response.content)
        
        print(f"Ghibli-style image saved to: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python ghibli_converter.py <image_path> [prompt] [output_dir]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "ghibli_output"
    
    convert_to_ghibli_style(image_path, output_dir, prompt)

if __name__ == "__main__":
    main()