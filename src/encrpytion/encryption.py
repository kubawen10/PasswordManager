from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import CMAC

class Encryption:
    def __init__(self, password: str) -> None:
        self.password = password.encode()

    def encrypt(self, data: str):
        salt = get_random_bytes(16)
        key = PBKDF2(self.password, salt, dkLen=16, count=100000)
        cipher = AES.new(key, AES.MODE_CBC)
        
        ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
        
        cmac = CMAC.new(key, ciphermod=AES)
        cmac.update(ciphertext)
        mac = cmac.digest()

        return salt + mac + cipher.iv + ciphertext

    def decrypt(self, encrypted_data: bytes):
        salt = encrypted_data[:16]
        mac = encrypted_data[16:32]
        iv = encrypted_data[32:48]
        ciphertext = encrypted_data[48:]

        key = PBKDF2(self.password, salt, dkLen=16, count=100000)

        cmac = CMAC.new(key, ciphermod=AES)
        cmac.update(ciphertext)
        cmac.verify(mac)

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return plaintext.decode()
