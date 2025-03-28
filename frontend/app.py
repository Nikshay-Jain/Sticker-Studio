import streamlit as st
import os
from model import generate_sticker

# Ensure directories exist
UPLOAD_DIR = "uploaded_images"
OUTPUT_DIR = "stickers"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.title("AI Sticker Studio 🎨")

# Take inputs
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
text_input = st.text_input("Enter Caption for the sticker:")
style = st.selectbox("Choose Style:", ["Original", "Ghibli"])
color = st.color_picker("Pick a Text Color", "#FFFFFF")

# Font options (Google Fonts for UI, Local TTF for PIL)
font_options = {
    "Bangers": "https://fonts.googleapis.com/css2?family=Bangers&display=swap",
    "Lobster": "https://fonts.googleapis.com/css2?family=Lobster&display=swap",
    "Pacifico": "https://fonts.googleapis.com/css2?family=Pacifico&display=swap",
    "Fredoka One": "https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap",
    "Anton": "https://fonts.googleapis.com/css2?family=Anton&display=swap"
}

# Mapping display names to actual font file names
font_files = {
    "Bangers": "Bangers-Regular",
    "Lobster": "Lobster-Regular",
    "Pacifico": "Pacifico-Regular",
    "Fredoka One": "FredokaOne-Regular",
    "Anton": "Anton-Regular"
}

st.markdown("### Choose Font Style:")
selected_font = st.radio("Select Font Style:", list(font_options.keys()), horizontal=True)

# Load the selected font for UI display
font_url = font_options[selected_font]
st.markdown(f'<link href="{font_url}" rel="stylesheet">', unsafe_allow_html=True)

# Show the font preview in its actual style
st.markdown(
    f"""
    <p style="
    font-family: '{selected_font}', cursive;
    font-size: 28px;
    color: {color};
    text-align: center;
    ">
    {text_input if text_input else "Your Text Here"}
    </p>
    """,
    unsafe_allow_html=True
)

# Generate Button
if st.button("Generate Sticker"):
    if uploaded_file and text_input:
        # Save uploaded image
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Get correct font filename
        font_filename = font_files[selected_font]

        # Process the image
        output_path = generate_sticker(file_path, text_input, style, color, font_filename)

        if os.path.exists(output_path):  # Ensure file exists before displaying
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