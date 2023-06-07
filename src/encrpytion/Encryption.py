from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Hash import SHA256

class Encryption:
    def __init__(self, key: str) -> None:
        self.key = key

    def hash_key(self):
        return SHA256.new(self.key.encode()).digest()

    def get_cipher(self, iv = None):
        key = self.hash_key()
        if iv:
            return AES.new(key, AES.MODE_CBC, iv=iv)
        else:
            return AES.new(key, AES.MODE_CBC)

    def encrytp(self, data: str) -> bytes:
        data = data.encode()

        cipher = self.get_cipher()
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))

        return base64.b64encode(cipher.iv + encrypted_data)


    def decrypt(self, encrypted_data: bytes) -> str:
        data = base64.b64decode(encrypted_data)

        iv = data[:AES.block_size]
        encrypted_data = data[AES.block_size:]

        cipher = self.get_cipher(iv=iv)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size).decode()

# c = Encryption('klucz')

# data = 'secret data test test test test test test'

# e = c.encrytp(data)

# print(c.decrypt(e))