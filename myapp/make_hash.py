from cryptography.fernet import MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64

# salt = os.urandom(16)
salt = b'aaaaa'


def hash_password(password):
    
    print('登録時の', salt)
    binary_password = password.encode('utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = kdf.derive(binary_password)
    print('key', key)
    return key


def verify_password(password, hashed_password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    print('確認時の', salt)
    print(password)
    print(hashed_password)
    
    # key = bytes(kdf.derive(binary_password))
    # print('key', key)
    # print(hashed_password)
    # if key == hashed_password:
    #     print('一致')
    #     return True
    # else:
    #     print('不一致')
    #     return False

    binary_password = password.encode('utf-8')
    print(hashed_password, type(hashed_password))
    hashed_password = bytes.fromhex(hashed_password[2:])
    print(binary_password)
    print(hashed_password, type(hashed_password))
    
    try:
        kdf.verify(binary_password, hashed_password)
        print('passwordが一致しました')
        return True
    except Exception:
        print('passwordが一致しません')
        return False


if __name__ == '__main__':
    password = 'sample'
    hashed_password = hash_password(password)
    print(hash_password)

    li = []
    li.append(hashed_password)

    verify_password('sample', li[0])
    print(password)