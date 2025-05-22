import base64
import hashlib
import requests
from io import BytesIO
from PIL import Image


api_key = 'sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN'
# tenant
tenant = "https://faircraft.benchling.com"

if __name__ == '__main__':

    # Load image from a file path
    image_path = "data/img.png"
    image = Image.open(image_path)

    # Convert image to binary format in memory
    byteImgIO = BytesIO()
    image.save(byteImgIO, format="PNG")  # Save image to the BytesIO buffer as PNG
    image_data = byteImgIO.getvalue()  # Get raw bytes

    # Encode image in base64 for safe transmission
    b64_image = base64.b64encode(image_data).decode('ascii')

    # Compute MD5 hash of the image (required by Benchling)
    md5_hasher = hashlib.md5()
    md5_hasher.update(image_data)
    md5 = md5_hasher.hexdigest()

    # Prepare request body
    blob_request_body = {
        "name": "uploaded_image.png",
        "type": "VISUALIZATION",  # the blob will be displayed as an image preview in the Benchling UI
        "data64": b64_image,
        "md5": md5
    }

    # Send the POST request to upload the image blob
    response = requests.post(
        f"{tenant}/api/v2/blobs",
        auth=(api_key, ""),
        json=blob_request_body
    )

    # Parse response
    if response.status_code == 200:
        response_json = response.json()
        plot_id = response_json["id"] # Persist blob_id
        print(f"✅ Image uploaded successfully! Blob ID: {plot_id}")
    else:
        print(f"❌ Upload failed. Status code: {response.status_code}")
        print(response.text)




