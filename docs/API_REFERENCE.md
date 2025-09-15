# API Reference

## Receipt Detection API

The Receipt Detection API provides a RESTful interface for detecting receipts in images using a trained Mask R-CNN model.

### Base URL
```
http://127.0.0.1:8888
```

### Endpoints

#### POST /predict

Detect receipts in an uploaded image.

**Request:**
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Body:**
  - `image` (file): Image file to process (supports JPG, PNG, WEBP, etc.)

**Response:**
```json
{
  "boxes": [
    [x1, y1, x2, y2],
    [x1, y1, x2, y2]
  ],
  "scores": [0.95, 0.87],
  "labels": [1, 1]
}
```

**Response Fields:**
- `boxes`: List of bounding boxes in format [x1, y1, x2, y2]
- `scores`: List of confidence scores (0.0 to 1.0)
- `labels`: List of class labels (1 for receipt)

**Example cURL:**
```bash
curl -X POST "http://127.0.0.1:8888/predict" \
     -F "image=@path/to/image.jpg"
```

**Example Python:**
```python
import requests

url = "http://127.0.0.1:8888/predict"
with open("image.jpg", "rb") as f:
    files = {"image": f}
    response = requests.post(url, files=files)

result = response.json()
print(f"Found {len(result['boxes'])} receipts")
```

### Error Responses

**500 Internal Server Error:**
```json
{
  "detail": "Prediction failed: [error message]"
}
```

### Configuration

The API uses the following configuration (from `config.py`):
- **Model Path:** `models/model.pth`
- **Confidence Threshold:** 0.8
- **Device:** Auto-detected (CUDA if available, otherwise CPU)

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)
- BMP (.bmp)
- TIFF (.tiff)

### Performance Notes

- The API processes images in RGB format
- Images are automatically resized and normalized
- Bounding boxes are returned in the original image coordinates
- Overlapping detections are merged using IoU threshold of 0.1
