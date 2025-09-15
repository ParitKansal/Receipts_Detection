"""
Setup script for the Receipt Detection system.

This script helps set up the environment and verify the installation.
"""

import os
import sys
import subprocess
import requests
import time
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'torch', 'torchvision', 
        'PIL', 'numpy', 'requests', 'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_model_file():
    """Check if the model file exists."""
    print("\nChecking model file...")
    
    model_path = Path("models/model.pth")
    if model_path.exists():
        print(f"✅ Model file found: {model_path}")
        return True
    else:
        print(f"❌ Model file not found: {model_path}")
        print("Please ensure the trained model is in the models/ directory")
        return False

def check_directories():
    """Check if required directories exist."""
    print("\nChecking directory structure...")
    
    required_dirs = [
        "data/raw", "data/processed", "models", "examples", 
        "scripts", "docs", "src"
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} - Missing")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\nMissing directories: {', '.join(missing_dirs)}")
        print("Creating missing directories...")
        for dir_path in missing_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")
    
    return True

def test_api():
    """Test if the API is running."""
    print("\nTesting API...")
    
    try:
        response = requests.get("http://127.0.0.1:8888/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print("❌ API returned status code:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API is not running")
        print("Start the API with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def run_basic_test():
    """Run a basic test with a sample image."""
    print("\nRunning basic test...")
    
    # Check if test images exist
    test_images_dir = Path("data/raw")
    if not test_images_dir.exists() or not list(test_images_dir.glob("*")):
        print("❌ No test images found in data/raw/")
        print("Please add some test images to data/raw/")
        return False
    
    # Find first test image
    test_image = next(test_images_dir.glob("*"), None)
    if not test_image:
        print("❌ No test images found")
        return False
    
    print(f"Testing with image: {test_image}")
    
    try:
        with open(test_image, "rb") as f:
            files = {"image": f}
            response = requests.post("http://127.0.0.1:8888/predict", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Test successful!")
            print(f"   Found {len(result['boxes'])} receipts")
            if result['boxes']:
                print(f"   Confidence scores: {[f'{s:.2f}' for s in result['scores']]}")
            return True
        else:
            print(f"❌ Test failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main setup function."""
    print("Receipt Detection System Setup")
    print("=" * 40)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check directories
    dirs_ok = check_directories()
    
    # Check model file
    model_ok = check_model_file()
    
    # Check API
    api_ok = test_api()
    
    # Run basic test if API is running
    test_ok = False
    if api_ok:
        test_ok = run_basic_test()
    
    print("\n" + "=" * 40)
    print("Setup Summary:")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"Directories: {'✅' if dirs_ok else '❌'}")
    print(f"Model file: {'✅' if model_ok else '❌'}")
    print(f"API running: {'✅' if api_ok else '❌'}")
    print(f"Basic test: {'✅' if test_ok else '❌'}")
    
    if all([deps_ok, dirs_ok, model_ok]):
        print("\n🎉 Setup complete! System is ready to use.")
        if not api_ok:
            print("💡 Start the API with: python app.py")
    else:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
