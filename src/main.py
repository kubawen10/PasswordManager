from encrpytion.Encryption import Encryption

c = Encryption('klucz')

data = 'secret data test test test test test test'

e = c.encrytp(data)

print(c.decrypt(e))

# from Crypto.Cipher import AES
# from Crypto.Hash import SHA256
# import base64
# import json
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes

# def gen_key(key: str):
#     return SHA256.new(key.encode()).digest()

# data = 'secret data test test test test test test'.encode()
# key=gen_key('hejka')

# cipher = AES.new(key, AES.MODE_CBC)
# ct_bytes = cipher.encrypt(pad(data, AES.block_size))

# data = base64.b64encode(cipher.iv + ct_bytes)

# try:
#     data = base64.b64decode(data)
#     iv = data[:AES.block_size]
#     ct = data[AES.block_size:]
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     pt = unpad(cipher.decrypt(ct), AES.block_size)
#     print("The message was: ", pt.decode())
# except (ValueError, KeyError):
#     print("Incorrect decryption")