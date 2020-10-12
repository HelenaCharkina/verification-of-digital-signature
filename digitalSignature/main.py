
from digitalSignature.KeysGenerator import generate_keys
from digitalSignature.ElGamal import encrypt, decrypt

dataStr = "иванов|20.04.1996"
dataStrNew = "иванов|20.04.1997" # измененное сообщение


keys = generate_keys()
keys = keys['Keys']

r, s = encrypt(keys, dataStr)
decrypt = decrypt(keys, r, s, dataStr)
if decrypt:
    print("Подпись верна!")
else:
    print("Подпись не верна!!")

