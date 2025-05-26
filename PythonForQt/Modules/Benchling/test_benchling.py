import sys, base64
import hashlib
import requests

# Change to your API Key
api_key = '***************'

# Change to your tenant
tenant = "https://example.benchling.com"

# chunk = 5242881 # 5MB + 1 byte to make divisible by 3 to avoid b64 padding
chunk = 10485762 * 3  # 10MB + 2 byte to make divisible by 3 to avoid b64 padding


def read_in_chunks(file_object, chunk_size=chunk):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def b64_encode(data):
    return base64.b64encode(data).decode('ascii')


def md5_hash(data):
    md5_hasher = hashlib.md5()
    md5_hasher.update(data)
    return md5_hasher.hexdigest()


def start_mulitpart(filename):
    request_body = {
        "mimeType": "application/octet-stream",
        "name": filename,
        "type": "RAW_FILE"
    }

    response = requests.post(tenant + "/api/v2/blobs:start-multipart-upload", auth=(api_key, ""), json=request_body)
    return response.json()


def upload_part(part, md5, number, blob_id):
    request_body = {
        "data64": part,
        "md5": md5,
        "partNumber": number
    }
    response = requests.post(tenant + "/api/v2/blobs/" + blob_id + "/parts", auth=(api_key, ""), json=request_body)
    print(response)
    print(response.text)
    return response.json()


def complete_upload(blob_id, parts):
    request_body = {
        "parts": parts
    }
    response = requests.post(tenant + "/api/v2/blobs/" + blob_id + ":complete-upload", auth=(api_key, ""),
                             json=request_body)
    return response

if __name__ == '__main__':

    filename = 'Compound_160500001_161000000.xml.gz'
    f = open('Downloads/' + filename, 'rb')

    start_json = start_mulitpart(filename)
    print(start_json)
    blob_id = start_json['id']

    part_data = []

    part_num = 0
    for piece in read_in_chunks(f):
        part_num += 1
        b64 = b64_encode(piece)
        md5 = md5_hash(piece)
        json = upload_part(b64, md5, part_num, blob_id)
        part_data.append(json)

    resp = complete_upload(blob_id, part_data)

    print("\n\n\n" + "------------------------------------" + "\n")
    print(resp)
    print(resp.text)