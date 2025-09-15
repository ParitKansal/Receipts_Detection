# Usage Guide

## Quick Start

### 1. Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Receipts_Detection
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or using conda:
   ```bash
   conda env create -f environment.yml
   conda activate receipts
   ```

### 2. Start the API Server

```bash
python app.py
```

The API will be available at `http://127.0.0.1:8888`

### 3. Test with an Image

```python
import requests

# Test with a sample image
url = "http://127.0.0.1:8888/predict"
with open("data/raw/unnamed (1).webp", "rb") as f:
    files = {"image": f}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print(f"Found {len(result['boxes'])} receipts")
    for i, (box, score) in enumerate(zip(result['boxes'], result['scores'])):
        print(f"Receipt {i+1}: confidence={score:.2f}, box={box}")
else:
    print(f"Error: {response.status_code}")
```

## Examples

### Basic Usage

See `examples/basic_usage.py` for a complete example:

```python
from examples.basic_usage import detect_receipts, crop_receipts

# Detect receipts in an image
result = detect_receipts("data/raw/unnamed (1).webp")

# Crop detected receipts
crop_receipts("data/raw/unnamed (1).webp", result)
```

### Batch Processing

Process multiple images at once:

```python
from examples.batch_processing import process_batch

# Process all images in data/raw directory
process_batch()
```

### Using the API Client

For more advanced usage, use the provided client class:

```python
from examples.api_client import ReceiptDetectionClient

client = ReceiptDetectionClient()

# Detect receipts
result = client.detect_receipts("image.jpg")

# Get summary statistics
summary = client.get_detection_summary(result)
print(f"Found {summary['count']} receipts")

# Crop receipts
cropped_paths = client.crop_receipts("image.jpg", result)
```

## Input/Output Examples

### Input Images

The system works with various receipt formats:
- Single receipts
- Multiple receipts per page
- Handwritten receipts
- Scanned documents
- Photos of receipts

### Output Format

The API returns JSON with the following structure:

```json
{
  "boxes": [
    [100, 150, 400, 600],
    [500, 200, 800, 700]
  ],
  "scores": [0.95, 0.87],
  "labels": [1, 1]
}
```

Where:
- `boxes[i]` = [x1, y1, x2, y2] coordinates of bounding box
- `scores[i]` = confidence score (0.0 to 1.0)
- `labels[i]` = class label (1 for receipt)

### Cropping Receipts

To crop detected receipts from the original image:

```python
from PIL import Image

# Load original image
image = Image.open("original.jpg")

# For each detected receipt
for box in result['boxes']:
    x1, y1, x2, y2 = map(int, box)
    cropped = image.crop((x1, y1, x2, y2))
    cropped.save(f"receipt_{i}.jpg")
```

## Configuration

### Model Settings

Edit `config.py` to modify:

- **Confidence Threshold:** Minimum confidence for detections (default: 0.8)
- **Model Path:** Path to the trained model file
- **Device:** CUDA/CPU selection

```python
CONFIDENCE_THRESHOLD = 0.8  # Adjust sensitivity
MODEL_PATH = "models/model.pth"  # Model file path
```

### API Settings

Modify `app.py` to change:

- **Host:** API host address (default: 0.0.0.0)
- **Port:** API port (default: 8888)

```python
uvicorn.run("app:app", host="0.0.0.0", port=8888)
```

## Troubleshooting

### Common Issues

1. **Model not found:**
   - Ensure `models/model.pth` exists
   - Check the path in `config.py`

2. **CUDA out of memory:**
   - The system will automatically fall back to CPU
   - For large images, consider resizing before processing

3. **API connection refused:**
   - Ensure the server is running (`python app.py`)
   - Check the port is not in use

4. **Low detection accuracy:**
   - Adjust `CONFIDENCE_THRESHOLD` in `config.py`
   - Ensure images are clear and well-lit
   - Try different image formats

### Performance Tips

1. **For batch processing:**
   - Process images sequentially to avoid memory issues
   - Use appropriate image sizes (not too large)

2. **For real-time processing:**
   - Keep the API server running
   - Use connection pooling for multiple requests

3. **For accuracy:**
   - Use high-quality images
   - Ensure receipts are clearly visible
   - Avoid heavily skewed or rotated images
