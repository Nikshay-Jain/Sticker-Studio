import streamlit as st
import os
from model import generate_sticker

# Ensure directories exist
UPLOAD_DIR = "uploads"
STATIC_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

st.title("AI Sticker Studio 🎨")

# Take inputs
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
text_input = st.text_input("Enter Caption for the sticker:")
style = st.selectbox("Choose Style:", ["Original", "Ghibli"])

# Generate Button
if st.button("Generate Sticker"):
    if uploaded_file and text_input:
        # Save uploaded image
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the image
        output_filename = generate_sticker(file_path, text_input, style)
        output_path = os.path.join(STATIC_DIR, output_filename)

        if output_filename:
            st.success("Sticker generated successfully! 🎉")
            st.image(output_path, caption="Generated Sticker", use_column_width=True)

            # Download button
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download Sticker",
                    data=file,
                    file_name="sticker.png",
                    mime="image/png"
                )
        else:
            st.error("Failed to generate sticker. Please try again.")