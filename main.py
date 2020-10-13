import json

import keras
from PIL import Image
from digitalSignature.ElGamal import decrypt, encrypt
from digitalSignature.KeysGenerator import generate_keys
from digitalSignature.types import Keys

from neural.GetString import get_string
from neural.Neural import create_cnn
from neural.TrainNeural import train_model
from pictureCropper.CropImage import crop_image

# --------Получение картинок данных-------------------
with open("coordinates.json", "r") as read_file:
    data = json.load(read_file)

img = Image.open("source/new_sign.jpg")

coordinates = data["fields"]
count_imgs = len(coordinates)
for coordinate in coordinates:
    crop_image(img, coordinate, count_imgs)


# --------Обучение-------------------
# model = create_cnn()
# train_model(model)
# model.save('neural/model/model.h5')

# --------Распознавание-------------------
count_imgs = 7
model = keras.models.load_model('neural/model/model.h5')
msg = ""
for i in range(count_imgs - 2):
    msg += get_string(model, "dataImages/" + (i + 1).__str__() + ".png")
    msg += "|"

r = int(get_string(model, "dataImages/r.png"))
s = int(get_string(model, "dataImages/s.png"))


# --------Генерация ключей-------------------
# keys = generate_keys()
# keys = keys['Keys']
# data = {
#     'p': keys.p,
#     'g': keys.g,
#     'public_key': keys.public_key
# }
#
# with open("keys.json", "w") as write_file:
#     json.dump(data, write_file)


# #--------Подпись-------------------
# keys = generate_keys()
# keys = keys['Keys']
#
# r, s = encrypt(keys, msg) # здесь нужен закрытый ключ
# data = {
#     'p': keys.p,
#     'g': keys.g,
#     'public_key': keys.public_key
# }
#
# with open("keys.json", "w") as write_file:
#     json.dump(data, write_file)
#
# print("r ", r)
# print("s ", s)

#
# #--------Проверка подписи-------------------
#
with open("keys.json", "r") as read_file:
    data = json.load(read_file)

keys = Keys()
keys.p = data["p"]
keys.g = data["g"]
keys.public_key = data["public_key"]

decrypt = decrypt(keys, r, s, msg)
print(decrypt)
