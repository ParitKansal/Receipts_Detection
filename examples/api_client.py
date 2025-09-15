"""
API Client class for Receipt Detection.

This module provides a convenient Python client for interacting
with the Receipt Detection API.
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
from PIL import Image
import io

class ReceiptDetectionClient:
    """
    Client for the Receipt Detection API.
    
    This class provides methods to interact with the receipt detection
    API and process the results.
    """
    
    def __init__(self, api_url: str = "http://127.0.0.1:8888/predict"):
        """
        Initialize the API client.
        
        Args:
            api_url (str): The API endpoint URL
        """
        self.api_url = api_url
        self.session = requests.Session()
    
    def detect_receipts(self, image_path: str) -> Optional[Dict]:
        """
        Detect receipts in an image file.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict containing boxes, scores, and labels, or None if failed
        """
        try:
            with open(image_path, "rb") as f:
                files = {"image": f}
                response = self.session.post(self.api_url, files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def detect_receipts_from_pil(self, image: Image.Image) -> Optional[Dict]:
        """
        Detect receipts from a PIL Image object.
        
        Args:
            image (PIL.Image): PIL Image object
            
        Returns:
            Dict containing boxes, scores, and labels, or None if failed
        """
        try:
            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            files = {"image": ("image.png", img_byte_arr, "image/png")}
            response = self.session.post(self.api_url, files=files)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def crop_receipts(self, image_path: str, detection_result: Dict, 
                     output_dir: str = "data/processed") -> List[str]:
        """
        Crop detected receipts from the original image.
        
        Args:
            image_path (str): Path to the original image
            detection_result (Dict): Detection results from API
            output_dir (str): Directory to save cropped images
            
        Returns:
            List of paths to saved cropped images
        """
        if not detection_result:
            return []
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Load the original image
        image = Image.open(image_path).convert("RGB")
        
        boxes = detection_result.get("boxes", [])
        scores = detection_result.get("scores", [])
        
        cropped_paths = []
        
        # Crop each detected receipt
        for i, (box, score) in enumerate(zip(boxes, scores)):
            x1, y1, x2, y2 = map(int, box)
            
            # Crop the bounding box
            cropped_image = image.crop((x1, y1, x2, y2))
            
            # Save the cropped image
            output_filename = f"receipt_{i+1}_score_{score:.2f}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            cropped_image.save(output_path)
            
            cropped_paths.append(output_path)
        
        return cropped_paths
    
    def get_detection_summary(self, detection_result: Dict) -> Dict:
        """
        Get a summary of detection results.
        
        Args:
            detection_result (Dict): Detection results from API
            
        Returns:
            Dict containing summary statistics
        """
        if not detection_result:
            return {"count": 0, "avg_confidence": 0, "max_confidence": 0, "min_confidence": 0}
        
        boxes = detection_result.get("boxes", [])
        scores = detection_result.get("scores", [])
        
        if not scores:
            return {"count": 0, "avg_confidence": 0, "max_confidence": 0, "min_confidence": 0}
        
        return {
            "count": len(boxes),
            "avg_confidence": sum(scores) / len(scores),
            "max_confidence": max(scores),
            "min_confidence": min(scores)
        }

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = ReceiptDetectionClient()
    
    # Example image path
    image_path = "data/raw/unnamed (1).webp"
    
    print("Receipt Detection API Client Example")
    print("=" * 40)
    
    # Detect receipts
    result = client.detect_receipts(image_path)
    
    if result:
        # Print summary
        summary = client.get_detection_summary(result)
        print(f"Detection Summary:")
        print(f"  Receipts found: {summary['count']}")
        print(f"  Average confidence: {summary['avg_confidence']:.2f}")
        print(f"  Max confidence: {summary['max_confidence']:.2f}")
        print(f"  Min confidence: {summary['min_confidence']:.2f}")
        
        # Crop receipts
        cropped_paths = client.crop_receipts(image_path, result)
        print(f"\nCropped {len(cropped_paths)} receipt(s):")
        for path in cropped_paths:
            print(f"  - {path}")
    else:
        print("Detection failed!")
