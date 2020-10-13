import json

from PIL import Image

from pictureCropper.CropImage import crop_image

with open("../coordinates.json", "r") as read_file:
    data = json.load(read_file)

img = Image.open("source/img.png")

coordinates = data["fields"]
for coordinate in coordinates:
    print(coordinate)
    crop_image(img, coordinate)



