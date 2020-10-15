import json

import cv2
import keras
from PIL import Image
from digitalSignature.ElGamal import encrypt, decrypt
from digitalSignature.KeysGenerator import generate_keys
from digitalSignature.types import Keys
from imageSigner.imageSigner import sign_image
from neural.GetString import get_string
from neural.Neural import create_cnn
from neural.TrainNeural import train_model
from pictureCropper.CropImage import crop_image


def sign(file_name):
    with open("coordinates.json", "r") as read_file:
        data = json.load(read_file)

    img = Image.open(file_name)

    coordinates = data["fields"]
    count_imgs = len(coordinates)
    for coordinate in coordinates:
        crop_image(img, coordinate, count_imgs)

    model = keras.models.load_model('neural/model/model.h5')
    msg = ""
    for i in range(count_imgs - 2):
        msg += get_string(model, "dataImages/" + (i + 1).__str__() + ".png")
        msg += "|"

    keys = generate_keys()
    keys = keys['Keys']

    r, s = encrypt(keys, msg)  # здесь нужен закрытый ключ
    data = {
        'p': keys.p,
        'g': keys.g,
        'public_key': keys.public_key
    }

    with open("keys.json", "w") as write_file:
        json.dump(data, write_file)

    print("r ", r)
    print("s ", s)

    sign_img = cv2.imread(file_name)

    x = coordinates[len(coordinates) - 1]["x"]
    y = coordinates[len(coordinates) - 1]["y"]
    height = coordinates[len(coordinates) - 1]["height"]
    width = coordinates[len(coordinates) - 1]["width"]
    widthImg, heightImg = img.size

    sign_image(sign_img, str(r), int(x * widthImg), int(y * widthImg + height * widthImg / 2),
               width * widthImg / len(str(r)) / 20) #todo
    sign_image(sign_img, str(s), int(x * widthImg), int(y * widthImg + height * widthImg),
               width * widthImg / len(str(r)) / 20) #todo


def check(file_name):
    with open("coordinates.json", "r") as read_file:
        data = json.load(read_file)

    img = Image.open(file_name)

    coordinates = data["fields"]
    count_imgs = len(coordinates)
    for coordinate in coordinates:
        crop_image(img, coordinate, count_imgs)

    model = keras.models.load_model('neural/model/model.h5')
    msg = ""
    for i in range(count_imgs - 2):
        msg += get_string(model, "dataImages/" + (i + 1).__str__() + ".png")
        msg += "|"
    r = int(get_string(model, "dataImages/r.png"))
    s = int(get_string(model, "dataImages/s.png"))
    print("r ", r)
    print("s ", s)

    with open("keys.json", "r") as read_file:
        data = json.load(read_file)

    keys = Keys()
    keys.p = data["p"]
    keys.g = data["g"]
    keys.public_key = data["public_key"]

    ok = decrypt(keys, r, s, msg)
    return ok


# --------Обучение-------------------
# model = create_cnn()
# train_model(model)
#model.save('neural/model/model.h5')

# --------Распознавание-------------------
# model = keras.models.load_model('neural/model/model.h5')
# msg = ""
# for i in range(count_imgs - 2):
#     msg += get_string(model, "dataImages/" + (i + 1).__str__() + ".png")
#     msg += "|"

# r = int(get_string(model, "dataImages/rscan.png"))
# s = int(get_string(model, "dataImages/sscan.png"))


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

##--------------Вставляем подпись в файл------------------------

# sign_img = cv2.imread(source)
#
# x = coordinates[len(coordinates) - 1]["x"]
# y = coordinates[len(coordinates) - 1]["y"]
# height = coordinates[len(coordinates) - 1]["height"]
# width = coordinates[len(coordinates) - 1]["width"]
# widthImg, heightImg = img.size
#
# sign_image(sign_img, str(r), int(x * widthImg), int(y * widthImg + height * widthImg / 2), width * widthImg / len(str(r)) / 20)
# sign_image(sign_img, str(s), int(x * widthImg), int(y * widthImg + height * widthImg ), width * widthImg / len(str(r)) / 20)
#
# #--------Проверка подписи-------------------
#
# with open("keys.json", "r") as read_file:
#     data = json.load(read_file)
#
# keys = Keys()
# keys.p = data["p"]
# keys.g = data["g"]
# keys.public_key = data["public_key"]
#
# decrypt = decrypt(keys, r, s, msg)
# if decrypt:
#     print("Подпись верна!")
# else:
#     print("Подпись не верна!")
