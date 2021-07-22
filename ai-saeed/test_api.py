import requests 
import base64
import cv2
from PIL import Image
from io import BytesIO


image_url = "http://risos.hadeth.ir/mediafiles/test.jpeg"

url = "http://127.0.0.1:4557" 
data = {
  "url": image_url,
}
response = requests.post(url,json=data)

img_data = response.json()["image"]
print(response.headers)
# img_data = "data:image/jpeg;base64, " + img_data
print(img_data[:100])
# print(img_data[-1:-1000])
# data = ContentFile(base64.b64decode(img_data), name='temp.' + ext)

# Write to a file to show conversion worked
data = base64.b64decode(img_data)
with open("imageToSave.png", "wb") as fh:
    fh.write(data)



data = cv2.imread("imageToSave.png")
print(data)