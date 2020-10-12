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

#--------Получение картинок данных-------------------
# with open("pictureCropper/coordinates.json", "r") as read_file:
#     data = json.load(read_file)
#
# img = Image.open("source/img.png")
#
# coordinates = data["fields"]
# for coordinate in coordinates:
#     crop_image(img, coordinate)

#--------Обучение-------------------
# model = create_cnn()
# train_model(model)
# model.save('neural/model/model.h5')

#--------Распозавание-------------------
model = keras.models.load_model('neural/model/model.h5')
#result = get_string(model, "dataImages/3.png")
result = get_string(model, "test digit/0.png")
print(result)

#--------Генерация ключей-------------------
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
# r, s = encrypt(keys, result) # здесь нужен закрытый ключ
# data = {
#     'p': keys.p,
#     'g': keys.g,
#     'public_key': keys.public_key
# }
#
# with open("keys.json", "w") as write_file:
#     json.dump(data, write_file)
#
# #--------Проверка подписи-------------------
# with open("keys.json", "r") as read_file:
#     data = json.load(read_file)
#
# keys = Keys()
# keys.p = data["p"]
# keys.g = data["g"]
# keys.public_key = data["public_key"]
#
# decrypt = decrypt(keys, r, s, result)


