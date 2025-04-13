import logging

def theme_convertor(image_path, theme, log_filename):
    """Processes the image and generates a sticker."""
    # Configure logging to use the same file as the Streamlit app
    if log_filename:
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # Dummy converting logic (replace with actual code)
    themed_seg_img_path = image_path

    return themed_seg_img_path

import pyautogui
import time
import os

class GrokImageConverterGUI:
    def __init__(self):
        self.output_dir = r"C:\Users\niksh\Desktop\Ghibli-Sticker-Studio\grok_output_images_gui"
        os.makedirs(self.output_dir, exist_ok=True)

    def open_edge_and_navigate_to_grok(self, grok_url="https://grok.com/chat/c6a8facb-f82c-46ba-be6b-379d0957bd2a"):
        print("Attempting to open Edge and navigate to Grok...")

        # Press the Windows key
        pyautogui.press('win')
        time.sleep(1)

        # Type "edge"
        pyautogui.write('edge')
        time.sleep(1.5)  # Give time for the search results to appear

        # Press Enter to open Microsoft Edge
        pyautogui.press('enter')
        time.sleep(1)  # Wait for Edge to open

        # **YOU MIGHT NEED TO ADJUST THE COORDINATES FOR THE ADDRESS BAR**
        address_bar_x = 309
        address_bar_y = 70

        pyautogui.moveTo(address_bar_x, address_bar_y, duration=1)
        pyautogui.click()
        pyautogui.write(grok_url)
        pyautogui.press('enter')
        time.sleep(3)
        print("Navigated to Grok. Please ensure you are logged in.")
        # input("Press Enter once you are logged in to Grok...")
        return True

    def upload_image_and_prompt(self, image_path, prompt):
        print("Attempting to upload image and enter prompt...")
        if not os.path.exists(image_path):
            print(f"Image not found at path: {image_path}")
            return False

        # **YOU WILL NEED TO FIND THE COORDINATES FOR THE IMAGE UPLOAD BUTTON ON GROK**
        upload_button_x = 509
        upload_button_y = 1024

        pyautogui.moveTo(upload_button_x, upload_button_y, duration=1)
        pyautogui.click()
        time.sleep(2) # Wait for the file dialog

        upload_button_x_2 = 576
        upload_button_y_2 = 922

        pyautogui.moveTo(upload_button_x_2, upload_button_y_2, duration=1)
        pyautogui.click()
        time.sleep(2) # Wait for the file dialog

        # Type the image path into the file dialog
        pyautogui.write(image_path)
        time.sleep(3)
        pyautogui.press('enter')
        time.sleep(5) # Wait for the image to upload

        # **YOU WILL NEED TO FIND THE COORDINATES FOR THE PROMPT INPUT FIELD**
        prompt_field_x = 847 # Example X coordinate, adjust as needed
        prompt_field_y = 956 # Example Y coordinate, adjust as needed

        pyautogui.moveTo(prompt_field_x, prompt_field_y, duration=1)
        pyautogui.click()
        pyautogui.write(prompt)
        time.sleep(3)

        pyautogui.press('enter')
        time.sleep(45) # Wait for the Ghibli image to be generated. Adjust as needed.
        print("Image uploaded and prompt entered. Waiting for output...")
        return True

    def save_output_image(self):
        print("Attempting to save the output image...")
        # **YOU WILL NEED TO FIND THE COORDINATES OF THE GENERATED IMAGE ON GROK**
        output_image_x = 1152 # Example X coordinate, adjust as needed
        output_image_y = 535 # Example Y coordinate, adjust as needed

        pyautogui.moveTo(output_image_x, output_image_y, duration=1)
        pyautogui.rightClick()
        time.sleep(1)

        # **YOU WILL NEED TO FIND THE COORDINATES FOR "Save image as..." in the context menu**
        save_as_x = 1158 # Example X coordinate, adjust as needed
        save_as_y = 535 # Example Y coordinate, adjust as needed

        pyautogui.moveTo(save_as_x, save_as_y, duration=1)
        pyautogui.click()
        time.sleep(2) # Wait for the save dialog

        output_filename = os.path.join(self.output_dir, "grok_ghibli_output.png")
        pyautogui.write(output_filename)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(3)
        print(f"Output image saved to: {output_filename}")
        return output_filename

def main():
    converter = GrokImageConverterGUI()

    if not converter.open_edge_and_navigate_to_grok():
        return

    image_path = r"C:\Users\niksh\Desktop\test2.png"
    prompt = "Convert this image to a Ghibli style in HD."

    if not converter.upload_image_and_prompt(image_path, prompt):
        return

    output_image_path = converter.save_output_image()
    if output_image_path:
        print(f"Ghibli image saved at: {output_image_path}")
    else:
        print("Failed to save the Ghibli image.")

if __name__ == "__main__":
    main()