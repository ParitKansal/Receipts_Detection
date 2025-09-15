import requests
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# API Endpoint
url = "http://127.0.0.1:8888/predict"

# Input and Output Folders
input_folder = r"data\raw"
output_folder = r"data\processed"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
valid_ext = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

# Loop through all images in input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_ext):
        image_path = os.path.join(input_folder, filename)
        print(f"Processing: {filename}")

        # Send the POST Request
        with open(image_path, "rb") as f:
            files = {"image": f}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            response_data = response.json()
            boxes = response_data.get("boxes", [])
            scores = response_data.get("scores", [])

            # Open the Image
            image = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(image)

            # Draw each bounding box
            for box, score in zip(boxes, scores):
                x1, y1, x2, y2 = box
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                draw.text((x1, y1 - 10), f"{score:.2f}", fill="red")

            # Save the output image
            output_path = os.path.join(output_folder, filename)
            image.save(output_path)
            print(f"Saved annotated image: {output_path}")

        else:
            print(f"❌ Failed: {filename} - {response.status_code}, {response.text}")
