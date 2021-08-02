from cryptography.fernet import Fernet

def descrypt():
    key = open('token','rb').read()
    f = Fernet(key)
    with open('licencia','rb') as file:
        arch = file.read()
    des_data = f.decrypt(arch)
    return des_data.decode('utf-8')