import hashlib
from dotenv import load_dotenv
import os
import binascii
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(text : str) -> str:
    load_dotenv()
    SALT = (os.environ["SALT"]).encode()
    ITERATIONS = int(os.environ["ITERATIONS"])

    text = text.encode()

    encrypted = hashlib.pbkdf2_hmac("sha256", text, SALT, ITERATIONS)

    return binascii.hexlify(encrypted).decode()


def encrypt_password(key, source):
    key = SHA256.new(key).digest()
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source)
    return base64.b64encode(data).decode("latin-1")


def decrypt_password(key, source):
    source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()
    IV = source[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding]
