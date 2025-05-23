import base64
import hashlib
import requests
import json
from io import BytesIO
from PIL import Image


#---------------------------------------------------------------------#
API_KEY = 'sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN'
DOMAIN = "faircraft.benchling.com" # tenant
PATH = "blobs"
CHUNK_SIZE_BYTES = int(10e6)
#---------------------------------------------------------------------#
class BadRequestException(Exception):
    def __init__(self, message, rv):
        super(BadRequestException, self).__init__(message)
        self.rv = rv
#---------------------------------------------------------------------#
def api_post(domain, api_key, path, request_body):
    """
    POST API Call
    :param domain:
    :param api_key:
    :param path:
    :param request_body:
    :return: request in json format
    """
    url = "https://{}/api/v2/{}".format(domain, path)
    # Send the POST request to upload the image blob
    request = requests.post(url,
                       json=request_body,
                       auth=(api_key, ""))
    if request.status_code >= 400:
        raise BadRequestException(
            "Server returned status {}. Response:\n{}".format(
                request.status_code, json.dumps(request.json())
            ),
            request,
        )
    return request
def read_image(img_path):
    """
    - Load image from a file path
    - Convert image to binary format in memory
    :param img_path:
    :return:
    """
    image = Image.open(img_path)
    byteImgIO = BytesIO()
    image.save(byteImgIO, format="PNG")  # Save image to the BytesIO buffer as PNG
    image_data = byteImgIO.getvalue()  # Get raw bytes
    return image_data

def encode_base64(image_data):
    """
    Encode image in base64 for safe transmission
    :param image_data:
    :return:
    """
    b64_image = base64.b64encode(image_data).decode('ascii')
    return b64_image

def calculate_md5(image_data):
    """
    Compute MD5 hash of the image (required by Benchling)
    :param image_data:
    :return:
    """
    md5_hasher = hashlib.md5()
    md5_hasher.update(image_data)

    return md5_hasher.hexdigest()

def upload_single_part_blob(img_path, api_key, domain, name):

    image_data = read_image(img_path)
    b64_image = encode_base64(image_data)
    md5 = calculate_md5(image_data)
    # Prepare request body
    blob_request_body = {
        "name": name,
        "type": "VISUALIZATION",  # the blob will be displayed as an image preview in the Benchling UI # "RAW_FILE"
        #"mimeType": "application/octet-stream",
        "data64": b64_image,
        "md5": md5
    }
    response = api_post(domain, api_key, "blobs", blob_request_body)
    response_json = response.json()
    assert(response_json["uploadStatus"] == "COMPLETE")

    # Parse response
    if response.status_code == 200:
        blob_id = response_json["id"]  # Persist blob_id
        new_name = response_json["name"] # name
        print(f"✅ Image {new_name} uploaded successfully! Blob ID: {blob_id}")

        return blob_id , new_name
    else:
        print(f"❌ Upload failed. Status code: {response.status_code}")
        print(response.text)

        return "None" , "None"

def download_blob(blob_id, api_key, domain, output_path):
    """
    Download a blob file using its ID and save it to disk.
    :param blob_id: The ID of the blob to download
    :param api_key: Your Benchling API key
    :param domain: Your Benchling domain (e.g., 'faircraft.benchling.com')
    :param output_path: File path to save the downloaded image
    """
    url = f"https://{domain}/api/v2/blobs/{blob_id}/download"

    # Send a GET request — will follow the redirect and download the file
    response = requests.get(url, auth=(api_key, ""), allow_redirects=True)

    if response.status_code == 200:
        # Write binary content to file
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Blob downloaded successfully and saved to '{output_path}'")
    elif response.status_code == 302:
        print("➡️ Received redirect but did not follow it (unexpected).")
    else:
        # 404 Not Found
        print(f"❌ Failed to download blob. Status code: {response.status_code}")
        print(response.text)


if __name__ == '__main__':
    blob_id , name = upload_single_part_blob(img_path="data/img.png",
                                             api_key=API_KEY,
                                             domain=DOMAIN,
                                             name="Faircraft_image.png"
                                            )
    download_blob(blob_id=blob_id,
                  api_key=API_KEY,
                  domain=DOMAIN,
                  output_path=f"generated_data/new_{name}"
    )



