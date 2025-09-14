import requests
from PIL import Image, ImageDraw
import os

# API Endpoint and Input/Output Directories
url = "http://127.0.0.1:8888/predict"
image_dir = r"D:\projects\Receipts_Detection_OD-main\tests\test_images"
output_dir = r"D:\projects\Receipts_Detection_OD-main\tests\images_output"

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all images in the folder
for filename in os.listdir(image_dir):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        image_path = os.path.join(image_dir, filename)

        # Send POST request
        with open(image_path, "rb") as f:
            files = {"image": f}
            response = requests.post(url, files=files)

        # Check response
        if response.status_code == 200:
            response_data = response.json()
            boxes = response_data.get("boxes", [])
            scores = response_data.get("scores", [])

            # Open image
            image = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(image)

            # Draw boxes
            for box, score in zip(boxes, scores):
                x1, y1, x2, y2 = box
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                draw.text((x1, max(0, y1 - 10)), f"{score:.2f}", fill="red")

            # Save result
            output_path = os.path.join(output_dir, filename)
            image.save(output_path)
            print(f"✅ Saved: {output_path}")
        else:
            print(f"❌ Failed for {filename}: {response.status_code}, {response.text}")