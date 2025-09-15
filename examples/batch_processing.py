"""
Batch processing example for the Receipt Detection API.

This script demonstrates how to process multiple images
and save annotated results.
"""

import requests
import os
from PIL import Image, ImageDraw
import time

# Configuration
API_URL = "http://127.0.0.1:8888/predict"
INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/processed/batch_results"

# Supported image extensions
SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

def process_batch(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, api_url=API_URL):
    """
    Process all images in a directory and save annotated results.
    
    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory to save annotated results
        api_url (str): API endpoint URL
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files
    image_files = [f for f in os.listdir(input_dir) 
                   if f.lower().endswith(SUPPORTED_EXTENSIONS)]
    
    if not image_files:
        print(f"No supported image files found in {input_dir}")
        return
    
    print(f"Found {len(image_files)} image(s) to process")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for i, filename in enumerate(image_files, 1):
        image_path = os.path.join(input_dir, filename)
        print(f"[{i}/{len(image_files)}] Processing: {filename}")
        
        try:
            # Send request to API
            with open(image_path, "rb") as f:
                files = {"image": f}
                response = requests.post(api_url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                boxes = result.get("boxes", [])
                scores = result.get("scores", [])
                
                # Load and annotate image
                image = Image.open(image_path).convert("RGB")
                draw = ImageDraw.Draw(image)
                
                # Draw bounding boxes
                for box, score in zip(boxes, scores):
                    x1, y1, x2, y2 = map(int, box)
                    draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                    draw.text((x1, max(0, y1 - 15)), f"{score:.2f}", fill="red")
                
                # Save annotated image
                output_path = os.path.join(output_dir, f"annotated_{filename}")
                image.save(output_path)
                
                print(f"  ✅ Success: {len(boxes)} receipt(s) detected")
                print(f"  📁 Saved: {output_path}")
                successful += 1
                
            else:
                print(f"  ❌ Failed: HTTP {response.status_code}")
                print(f"  📝 Error: {response.text}")
                failed += 1
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            failed += 1
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
        print()
    
    # Summary
    print("=" * 50)
    print(f"Batch processing complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Results saved to: {output_dir}")

def main():
    """Main function to run batch processing."""
    print("Receipt Detection - Batch Processing")
    print("=" * 40)
    
    # Check if input directory exists
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        print("Please ensure you have images in the data/raw directory")
        return
    
    # Start batch processing
    process_batch()

if __name__ == "__main__":
    main()
