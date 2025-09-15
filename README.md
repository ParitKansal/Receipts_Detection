# Receipt Detection System

A robust receipt detection system using Mask R-CNN for automatic identification and extraction of receipts from images. The system provides both a REST API and Python client for easy integration.

## 🚀 Features

- **High Accuracy**: Mask R-CNN model trained for receipt detection
- **REST API**: FastAPI-based web service for easy integration
- **Batch Processing**: Process multiple images simultaneously
- **Multiple Formats**: Support for JPG, PNG, WEBP, and other image formats
- **Confidence Scoring**: Returns confidence scores for each detection
- **Box Merging**: Automatically merges overlapping detections
- **Easy Integration**: Simple Python client and examples

## 📁 Project Structure

```
Receipts_Detection/
├── app.py                 # FastAPI web server
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── environment.yml       # Conda environment
├── src/
│   ├── pipeline.py       # Core detection pipeline
│   └── post_processing.py # Post-processing utilities
├── models/
│   └── model.pth         # Trained Mask R-CNN model
├── examples/             # Usage examples
│   ├── basic_usage.py    # Basic detection example
│   ├── batch_processing.py # Batch processing example
│   └── api_client.py     # API client class
├── scripts/              # Utility scripts
│   ├── test_api.py       # API testing script
│   ├── test_bbox.py      # Bounding box testing
│   └── test_bbox_bulk.py # Bulk testing script
├── data/
│   ├── raw/              # Input test images
│   └── processed/        # Output images with annotations
├── docs/                 # Documentation
│   ├── API_REFERENCE.md  # API documentation
│   ├── USAGE_GUIDE.md    # Usage guide
│   ├── ARCHITECTURE.md   # System architecture
│   └── EXAMPLES.md       # Input/output examples
└── README.md             # This file
```

## 🛠️ Installation

### Option 1: Using pip

```bash
# Clone the repository
git clone <repository-url>
cd Receipts_Detection

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
# Clone the repository
git clone <repository-url>
cd Receipts_Detection

# Create conda environment
conda env create -f environment.yml
conda activate receipts
```

## 🚀 Quick Start

### 1. Start the API Server

```bash
python app.py
```

The API will be available at `http://127.0.0.1:8888`

### 2. Test with a Sample Image

```python
import requests

# Test API
url = "http://127.0.0.1:8888/predict"
with open("data/raw/unnamed (1).webp", "rb") as f:
    files = {"image": f}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print(f"Found {len(result['boxes'])} receipts")
    for i, (box, score) in enumerate(zip(result['boxes'], result['scores'])):
        print(f"Receipt {i+1}: confidence={score:.2f}, box={box}")
```

### 3. Run Examples

```bash
# Basic usage
python examples/basic_usage.py

# Batch processing
python examples/batch_processing.py

# API client example
python examples/api_client.py
```

## 📖 Usage Examples

### Basic Detection

```python
from examples.api_client import ReceiptDetectionClient

# Initialize client
client = ReceiptDetectionClient()

# Detect receipts
result = client.detect_receipts("image.jpg")

# Get summary
summary = client.get_detection_summary(result)
print(f"Found {summary['count']} receipts")

# Crop receipts
cropped_paths = client.crop_receipts("image.jpg", result)
```

### Batch Processing

```python
from examples.batch_processing import process_batch

# Process all images in data/raw directory
process_batch()
```

### API Integration

```python
import requests

# Single image detection
url = "http://127.0.0.1:8888/predict"
with open("receipt.jpg", "rb") as f:
    files = {"image": f}
    response = requests.post(url, files=files)

result = response.json()
```

## 🔧 Configuration

### Model Settings

Edit `config.py` to modify:

```python
CONFIDENCE_THRESHOLD = 0.8  # Minimum confidence for detections
MODEL_PATH = "models/model.pth"  # Path to trained model
```

### API Settings

Modify `app.py` to change:

```python
uvicorn.run("app:app", host="0.0.0.0", port=8888)
```

## 📚 Documentation

- **[API Reference](docs/API_REFERENCE.md)**: Complete API documentation
- **[Usage Guide](docs/USAGE_GUIDE.md)**: Detailed usage instructions
- **[Architecture](docs/ARCHITECTURE.md)**: System architecture overview
- **[Examples](docs/EXAMPLES.md)**: Input/output examples and test cases

## 🧪 Testing

### Run Test Scripts

```bash
# Test API endpoint
python scripts/test_api.py

# Test bounding box detection
python scripts/test_bbox.py

# Test bulk processing
python scripts/test_bbox_bulk.py
```

### Test Images

Test images are located in `data/raw/`:
- Single receipts
- Multiple receipts per page
- Handwritten receipts
- Complex documents

## 🔍 API Reference

### POST /predict

Detect receipts in an uploaded image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response:**
```json
{
  "boxes": [[x1, y1, x2, y2], ...],
  "scores": [0.95, 0.87, ...],
  "labels": [1, 1, ...]
}
```

## 🛠️ Development

### Project Structure

- `src/pipeline.py`: Core detection logic using Mask R-CNN
- `src/post_processing.py`: Box merging and IoU calculations
- `app.py`: FastAPI web server
- `config.py`: Configuration management

### Adding New Features

1. **New Detection Classes**: Modify model architecture in `src/pipeline.py`
2. **Custom Post-processing**: Add functions to `src/post_processing.py`
3. **API Endpoints**: Add new routes in `app.py`
4. **Configuration**: Update `config.py` for new settings

## 🚀 Deployment

### Production Deployment

```bash
# Using uvicorn with multiple workers
uvicorn app:app --host 0.0.0.0 --port 8888 --workers 4

# Using gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment

```dockerfile
FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8888"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- PyTorch and Torchvision for the deep learning framework
- FastAPI for the web framework
- Mask R-CNN implementation for object detection

## 📞 Support

For questions and support:
- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the examples in the `examples/` folder

---

**Note**: This system requires a trained model file (`models/model.pth`). Ensure the model file is present before running the system.
