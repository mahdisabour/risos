import requests
import base64 
image_url = "http://risos.hadeth.ir/mediafiles/test.jpeg"

url = "http://127.0.0.1:4557" 
data = {
  "url": image_url,
}
response = requests.post(url,json=data)
print(type(response.json()["image"]))

jpg_original = base64.b64decode(response.json()["image"])

# Write to a file to show conversion worked
with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decodebytes(jpg_original))