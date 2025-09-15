"""
Basic usage example for the Receipt Detection API.

This script demonstrates how to use the receipt detection API
to detect and crop receipts from images.
"""

import requests
import json
from PIL import Image
import os

# Configuration
API_URL = "http://127.0.0.1:8888/predict"
IMAGE_PATH = "data/raw/unnamed (1).webp"  # Example image path

def detect_receipts(image_path, api_url=API_URL):
    """
    Detect receipts in an image using the API.
    
    Args:
        image_path (str): Path to the input image
        api_url (str): API endpoint URL
        
    Returns:
        dict: API response containing boxes, scores, and labels
    """
    try:
        with open(image_path, "rb") as f:
            files = {"image": f}
            response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def crop_receipts(image_path, detection_result, output_dir="data/processed"):
    """
    Crop detected receipts from the original image.
    
    Args:
        image_path (str): Path to the original image
        detection_result (dict): Detection results from API
        output_dir (str): Directory to save cropped images
    """
    if not detection_result:
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the original image
    image = Image.open(image_path).convert("RGB")
    
    boxes = detection_result.get("boxes", [])
    scores = detection_result.get("scores", [])
    
    print(f"Found {len(boxes)} receipt(s) in the image")
    
    # Crop each detected receipt
    for i, (box, score) in enumerate(zip(boxes, scores)):
        x1, y1, x2, y2 = map(int, box)
        
        # Crop the bounding box
        cropped_image = image.crop((x1, y1, x2, y2))
        
        # Save the cropped image
        output_filename = f"receipt_{i+1}_score_{score:.2f}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        cropped_image.save(output_path)
        
        print(f"Saved cropped receipt: {output_path}")
        print(f"  Confidence score: {score:.2f}")
        print(f"  Bounding box: ({x1}, {y1}, {x2}, {y2})")

def main():
    """Main function to demonstrate receipt detection."""
    print("Receipt Detection Example")
    print("=" * 30)
    
    # Check if image exists
    if not os.path.exists(IMAGE_PATH):
        print(f"Image not found: {IMAGE_PATH}")
        print("Please ensure you have test images in the data/raw directory")
        return
    
    # Detect receipts
    print(f"Processing image: {IMAGE_PATH}")
    result = detect_receipts(IMAGE_PATH)
    
    if result:
        print(f"Detection successful!")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Crop detected receipts
        crop_receipts(IMAGE_PATH, result)
    else:
        print("Detection failed!")

if __name__ == "__main__":
    main()
