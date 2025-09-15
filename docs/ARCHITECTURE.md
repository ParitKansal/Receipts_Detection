# Architecture Overview

## System Architecture

The Receipt Detection system is built using a modular architecture with the following components:

```
Receipts_Detection/
├── app.py                 # FastAPI web server
├── config.py             # Configuration settings
├── src/
│   ├── pipeline.py       # Core detection pipeline
│   └── post_processing.py # Post-processing utilities
├── models/
│   └── model.pth         # Trained Mask R-CNN model
├── examples/             # Usage examples
├── scripts/              # Utility scripts
├── data/
│   ├── raw/              # Input images
│   └── processed/        # Output images
└── docs/                 # Documentation
```

## Core Components

### 1. Detection Pipeline (`src/pipeline.py`)

The `BillRoiPredictor` class handles the core detection logic:

- **Model Loading:** Loads pre-trained Mask R-CNN model
- **Image Preprocessing:** Converts PIL images to tensors
- **Inference:** Runs detection on input images
- **Post-processing:** Applies confidence thresholding and box merging

**Key Methods:**
- `__init__(model_path)`: Initialize predictor with model
- `predict_image(image)`: Detect receipts in PIL image
- `_load_model()`: Load and configure the neural network

### 2. Post-Processing (`src/post_processing.py`)

Utilities for refining detection results:

- **IoU Calculation:** Computes intersection over union for boxes
- **Box Merging:** Merges overlapping detections to reduce duplicates

**Key Functions:**
- `iou(box1, box2)`: Calculate IoU between two bounding boxes
- `merge_boxes_iteratively(boxes, iou_threshold)`: Merge overlapping boxes

### 3. Web API (`app.py`)

FastAPI-based REST API for serving predictions:

- **Endpoint:** `POST /predict`
- **Input:** Multipart form data with image file
- **Output:** JSON with bounding boxes, scores, and labels
- **Error Handling:** Comprehensive error responses

### 4. Configuration (`config.py`)

Centralized configuration management:

- **Model Path:** Location of trained model file
- **Confidence Threshold:** Minimum score for valid detections
- **Device Selection:** CUDA/CPU auto-detection
- **Logging:** Log file configuration

## Model Architecture

### Mask R-CNN

The system uses a Mask R-CNN (Region-based Convolutional Neural Network) model:

- **Backbone:** ResNet-50 with Feature Pyramid Network (FPN)
- **Task:** Object detection and instance segmentation
- **Classes:** 2 classes (background + receipt)
- **Input:** RGB images of any size
- **Output:** Bounding boxes, confidence scores, and segmentation masks

### Model Configuration

```python
# Model architecture
model = torchvision.models.detection.maskrcnn_resnet50_fpn(weights="DEFAULT")

# Custom head for 2 classes
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, 2)
model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, 256, 2)
```

## Data Flow

### 1. Input Processing

```
Image File → PIL Image → Tensor → Model Input
```

1. User uploads image via API
2. Image converted to PIL Image object
3. PIL Image converted to PyTorch tensor
4. Tensor normalized and batched for model

### 2. Detection Pipeline

```
Model Input → Mask R-CNN → Raw Predictions → Post-Processing → Final Results
```

1. Model processes input tensor
2. Raw predictions include boxes, scores, labels
3. Confidence thresholding filters low-confidence detections
4. Box merging removes overlapping detections
5. Results returned as JSON

### 3. Output Format

```json
{
  "boxes": [[x1, y1, x2, y2], ...],    # Bounding box coordinates
  "scores": [0.95, 0.87, ...],         # Confidence scores
  "labels": [1, 1, ...]                # Class labels (1 = receipt)
}
```

## Performance Characteristics

### Model Performance

- **Inference Time:** ~200-500ms per image (CPU), ~50-100ms (GPU)
- **Memory Usage:** ~2-4GB RAM, ~1-2GB VRAM (GPU)
- **Accuracy:** High precision for clear, well-lit receipts
- **Robustness:** Works with various receipt formats and orientations

### API Performance

- **Throughput:** ~10-20 requests/second (CPU), ~50-100 requests/second (GPU)
- **Latency:** ~200-1000ms per request (depending on image size)
- **Concurrency:** Single-threaded processing (can be scaled with load balancer)

## Scalability Considerations

### Horizontal Scaling

- **Load Balancer:** Distribute requests across multiple API instances
- **Model Caching:** Keep model loaded in memory for fast inference
- **Async Processing:** Use async/await for I/O operations

### Vertical Scaling

- **GPU Acceleration:** Significant speedup with CUDA-capable GPU
- **Memory Optimization:** Batch processing for multiple images
- **Model Optimization:** Quantization or pruning for faster inference

## Security Considerations

### Input Validation

- **File Type Checking:** Validate uploaded file types
- **Size Limits:** Enforce maximum file size limits
- **Malicious Content:** Basic file content validation

### Error Handling

- **Graceful Degradation:** Fallback to CPU if GPU unavailable
- **Input Sanitization:** Validate and sanitize all inputs
- **Logging:** Comprehensive error logging for debugging

## Deployment Options

### Development

```bash
python app.py
```

### Production

```bash
uvicorn app:app --host 0.0.0.0 --port 8888 --workers 4
```

### Docker

```dockerfile
FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8888"]
```

### Cloud Deployment

- **AWS:** EC2 with GPU instances, ECS for containerized deployment
- **GCP:** Compute Engine, Cloud Run for serverless
- **Azure:** Virtual Machines, Container Instances
