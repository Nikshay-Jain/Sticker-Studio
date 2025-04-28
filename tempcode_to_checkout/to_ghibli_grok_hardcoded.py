# from datetime import datetime
# import pyautogui
# import logging
# import time
# import os

# class GrokImageConverterGUI:
#     def __init__(self):
#         self.output_dir = r"C:\Users\niksh\Desktop\Ghibli-Sticker-Studio\ghibli_images"
#         os.makedirs(self.output_dir, exist_ok=True)
#         logging.info(f"GrokImageConverterGUI initialized. Output directory: {self.output_dir}")

#     def open_edge_and_navigate_to_grok(self, grok_url="https://grok.com/chat/c6a8facb-f82c-46ba-be6b-379d0957bd2a"):
#         logging.info("Attempting to open Edge and navigate to Grok...")
#         print("Attempting to open Edge and navigate to Grok...")

#         # Press the Windows key
#         logging.info("Pressing the Windows key.")
#         pyautogui.press('win')
#         time.sleep(1)

#         # Type "edge"
#         logging.info("Typing 'edge'.")
#         pyautogui.write('edge')
#         time.sleep(1.5)  # Give time for the search results to appear

#         # Press Enter to open Microsoft Edge
#         logging.info("Pressing Enter to open Edge.")
#         pyautogui.press('enter')
#         time.sleep(2)  # Wait for Edge to open

#         # **YOU MIGHT NEED TO ADJUST THE COORDINATES FOR THE ADDRESS BAR**
#         address_bar_x = 309
#         address_bar_y = 70

#         logging.info(f"Moving mouse to address bar coordinates: ({address_bar_x}, {address_bar_y}).")
#         pyautogui.moveTo(address_bar_x, address_bar_y, duration=1)
#         logging.info("Clicking on the address bar.")
#         pyautogui.click()
#         logging.info(f"Writing Grok URL: {grok_url}")
#         pyautogui.write(grok_url)
#         logging.info("Pressing Enter to navigate to Grok.")
#         pyautogui.press('enter')
#         time.sleep(3)
#         print("Navigated to Grok. Please ensure you are logged in.")
#         logging.info("Navigated to Grok. Waiting for user login.")
#         return True

#     def upload_image_and_prompt(self, image_path, prompt):
#         logging.info("Attempting to upload image and enter prompt...")
#         print("Attempting to upload image and enter prompt...")
#         if not os.path.exists(image_path):
#             logging.error(f"Image not found at path: {image_path}")
#             print(f"Image not found at path: {image_path}")
#             return False
#         logging.info(f"Image found at path: {image_path}")

#         # **YOU WILL NEED TO FIND THE COORDINATES FOR THE IMAGE UPLOAD BUTTON ON GROK**
#         upload_button_x = 509
#         upload_button_y = 1024

#         logging.info(f"Moving mouse to upload button coordinates: ({upload_button_x}, {upload_button_y}).")
#         pyautogui.moveTo(upload_button_x, upload_button_y, duration=1)
#         logging.info("Clicking the upload button.")
#         pyautogui.click()
#         time.sleep(2) # Wait for the file dialog
#         logging.info("Waiting for file dialog to appear.")

#         upload_button_x_2 = 576
#         upload_button_y_2 = 922

#         logging.info(f"Moving mouse to the second upload button coordinates: ({upload_button_x_2}, {upload_button_y_2}).")
#         pyautogui.moveTo(upload_button_x_2, upload_button_y_2, duration=1)
#         logging.info("Clicking the second upload button.")
#         pyautogui.click()
#         time.sleep(2) # Wait for the file dialog
#         logging.info("Waiting for file dialog to appear after second click.")

#         # Type the image path into the file dialog
#         logging.info(f"Typing image path into file dialog: {image_path}")
#         pyautogui.write(image_path)
#         time.sleep(3)
#         logging.info("Pressing Enter in the file dialog.")
#         pyautogui.press('enter')
#         time.sleep(4) # Wait for the image to upload
#         logging.info("Waiting for image to upload.")

#         # **YOU WILL NEED TO FIND THE COORDINATES FOR THE PROMPT INPUT FIELD**
#         prompt_field_x = 847
#         prompt_field_y = 956

#         logging.info(f"Moving mouse to prompt field coordinates: ({prompt_field_x}, {prompt_field_y}).")
#         pyautogui.moveTo(prompt_field_x, prompt_field_y, duration=1)
#         logging.info("Clicking on the prompt field.")
#         pyautogui.click()
#         logging.info(f"Writing prompt: {prompt}")
#         pyautogui.write(prompt)
#         time.sleep(4)

#         logging.info("Pressing Enter after writing the prompt.")
#         pyautogui.press('enter')
#         time.sleep(40) # Wait for the Ghibli image to be generated. Adjust as needed.
#         print("Image uploaded and prompt entered. Waiting for output...")
#         logging.info("Image uploaded and prompt entered. Waiting for output.")
#         return True

#     def save_output_image(self):
#         logging.info("Attempting to save the output image...")
#         print("Attempting to save the output image...")
#         # **YOU WILL NEED TO FIND THE COORDINATES OF THE GENERATED IMAGE ON GROK**
#         output_image_x = 1152
#         output_image_y = 535

#         logging.info(f"Moving mouse to output image coordinates: ({output_image_x}, {output_image_y}).")
#         pyautogui.moveTo(output_image_x, output_image_y, duration=1)
#         logging.info("Right-clicking on the output image.")
#         pyautogui.rightClick()
#         time.sleep(1)

#         # **YOU WILL NEED TO FIND THE COORDINATES FOR "Save image as..." in the context menu**
#         save_as_x = 1158
#         save_as_y = 535

#         logging.info(f"Moving mouse to 'Save image as...' coordinates: ({save_as_x}, {save_as_y}).")
#         pyautogui.moveTo(save_as_x, save_as_y, duration=1)
#         logging.info("Clicking 'Save image as...'")
#         pyautogui.click()
#         time.sleep(2) # Wait for the save dialog
#         logging.info("Waiting for the save dialog.")

#         output_filename = os.path.join(self.output_dir, f"grok_ghibli_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
#         logging.info(f"Typing output filename: {output_filename}")
#         pyautogui.write(output_filename)
#         time.sleep(2)
#         logging.info("Pressing Enter to save the image.")
#         pyautogui.press('enter')
#         time.sleep(3)
#         print(f"Output image saved to: {output_filename}")
#         logging.info(f"Output image saved to: {output_filename}")
#         return output_filename

def theme_convertor(image_path, log_filename):
    # """Processes the image and generates a sticker."""
    # # Configure logging to use the same file as the Streamlit app
    # if log_filename:
    #     logging.basicConfig(
    #         filename=log_filename,
    #         level=logging.INFO,
    #         format="%(asctime)s - %(levelname)s - %(message)s",
    #         datefmt="%Y-%m-%d %H:%M:%S"
    #     )
    #     logging.info(f"Logging configured to file: {log_filename}")

    # converter = GrokImageConverterGUI()

    # if not converter.open_edge_and_navigate_to_grok():
    #     logging.error("Failed to open Edge and navigate to Grok.")
    #     return

    # prompt = "Convert this image to a Ghibli style in HD."
    # logging.info(f"Using prompt: {prompt}")

    # if not converter.upload_image_and_prompt(image_path, prompt):
    #     logging.error("Failed to upload image and enter prompt.")
    #     return

    # themed_seg_img_path = converter.save_output_image()
    # if themed_seg_img_path:
    #     logging.info(f"Ghibli image saved at: {themed_seg_img_path}")
    #     print(f"Ghibli image saved at: {themed_seg_img_path}")
    # else:
    #     logging.error("Failed to save the Ghibli image.")
    #     print("Failed to save the Ghibli image.")

    # logging.info(f"theme_convertor function finished. Returning: {themed_seg_img_path}")
    return image_path

# if __name__ == "__main__":
#     os.makedirs("logs", exist_ok=True)
#     print(theme_convertor(r"C:\Users\niksh\Desktop\test_00.png", f"logs/studio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"))