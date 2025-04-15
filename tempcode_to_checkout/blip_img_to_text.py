from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load and preprocess the image
image_path = "test_01.png"  # Replace with your image path
raw_image = Image.open(image_path).convert('RGB')

# Prepare inputs
inputs = processor(raw_image, return_tensors="pt")

# Generate caption with adjusted parameters for more detail
out = model.generate(
    **inputs,
    max_new_tokens=100,       # Increase the maximum number of tokens
    num_beams=5,             # Use beam search with 5 beams
    no_repeat_ngram_size=2,   # Prevent repetition
    early_stopping=True
)

# Decode and print the caption
caption = processor.decode(out[0], skip_special_tokens=True)
print("Detailed Caption:", caption)