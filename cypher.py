from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import os

def create_key(algoritmo, longitud=256):
    if algoritmo == 'RSA':
        key = RSA.generate(longitud)
        pub_key = key.publickey().export_key()
        priv_key = key.export_key()
        with open("pub_key.pem", "wb") as f:
            f.write(pub_key)
        with open("pri_key.pem", "wb") as f:
            f.write(priv_key)
        print("Claves RSA creadas correctamente.")
    elif algoritmo == 'AES':
        key = os.urandom(longitud // 8)
        with open("aes_key.bin", "wb") as f:
            f.write(key)
        print("Clave AES creada correctamente.")
    else:
        print("Algoritmo no válido.")

def get_key(tipo, algoritmo):
    try: 
        if algoritmo == 'RSA':
            if tipo == 'pub': 
                with open('pub.key.pem', 'rb') as pkp: key=pkp.read(); pkp.close(); key=RSA.import_key(key)
            else: 
                with open('pri.key.pem', 'rb') as pkp: key=pkp.read(); pkp.close(); key=RSA.import_key(key)
        elif algoritmo == 'AES':
            with open("aes_key.bin", "rb") as f:
                key = f.read()
    except FileNotFoundError:
        create_key(algoritmo, int(input("Tamaño para la clave. ej: 1024, 4096 >> ")))
        key = get_key(tipo, algoritmo)
    return key

def cifrar(algoritmo, tipo, data):
    key = get_key('pub', algoritmo)
    if algoritmo == 'RSA':
        cipher_rsa = PKCS1_OAEP.new(key)
        ciphertext = cipher_rsa.encrypt(data)
        return ciphertext
    elif algoritmo == 'AES':
        if tipo == "txt":
            cipher_aes = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            print(ciphertext)
        if tipo == "file": 
            with open(data, 'rb') as file:
                filepath = data
                data = file.read()
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            length = 16 - (len(data) % 16)
            data += bytes([length]) * length
            ciphertext = cipher.encrypt(data)
            with open(f'{filepath}.bin', 'wb') as file_out:
                file_out.write(iv)
                file_out.write(ciphertext)
            print("Archivo cifrado correctamente.")
        else:
            print(ciphertext)
    else:
        print("Algoritmo no válido.")
        return None

def descifrar(algoritmo, tipo, data):
    key = get_key('pri', algoritmo)
    if algoritmo == 'RSA':
        cipher_rsa = PKCS1_OAEP.new(key)
        plaintext = cipher_rsa.decrypt(data)
        return plaintext.decode()
    elif algoritmo == 'AES':
        if tipo == "file":
            with open(data, 'rb') as file:
                iv = file.read(16)  # Leer el IV (vector de inicialización)
                ciphertext = file.read()
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = cipher.decrypt(ciphertext)
            padding_length = plaintext[-1]
            plaintext = plaintext[:-padding_length]
            with open(data[:-4], 'wb') as file_out:
                file_out.write(plaintext)
        else:
            cipher_aes = AES.new(key, AES.MODE_EAX)
            plaintext = cipher_aes.decrypt(data)
            print(plaintext.decode())
    else:
        print("Algoritmo no válido.")
        return None

#create_key('AES', 256)
descifrar('AES', 'file', 'test.txt.bin')
#descifrar_archivo_aes('test.txt.bin', get_key('---', 'AES'))
#descifrado = descifrar_texto('RSA', cifrado)
#print("Texto descifrado:", descifrado)
