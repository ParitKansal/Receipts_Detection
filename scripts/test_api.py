import requests

url = "http://127.0.0.1:8888/predict"
image_path = r"data\raw\unnamed (1).webp"

with open(image_path, "rb") as f:
    files = {"image": f}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
