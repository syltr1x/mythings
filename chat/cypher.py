from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import os

def crear_clave(algoritmo, longitud):
    if algoritmo == 'RSA':
        key = RSA.generate(longitud)
        pub_key = key.publickey().export_key()
        priv_key = key.export_key()
        with open("pub_key.pem", "wb") as f:
            f.write(pub_key)
        with open("priv_key.pem", "wb") as f:
            f.write(priv_key)
        print("Claves RSA creadas correctamente.")
    elif algoritmo == 'AES':
        key = os.urandom(longitud // 8)
        with open("aes_key.bin", "wb") as f:
            f.write(key)
        print("Clave AES creada correctamente.")
    else:
        print("Algoritmo no válido.")

def cifrar(algoritmo, texto_a_cifrar):
    if algoritmo == 'RSA':
        try:
            with open("pub_key.pem", "rb") as f:
                pub_key = RSA.import_key(f.read())
            cipher_rsa = PKCS1_OAEP.new(pub_key)
            ciphertext = cipher_rsa.encrypt(texto_a_cifrar.encode())
            return ciphertext
        except FileNotFoundError:
            print("No se encontró la clave pública RSA. Cree la clave primero.")
            return None
    elif algoritmo == 'AES':
        try:
            with open("aes_key.bin", "rb") as f:
                key = f.read()
            cipher_aes = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(texto_a_cifrar.encode())
            return ciphertext
        except FileNotFoundError:
            print("No se encontró la clave AES. Cree la clave primero.")
            return None
    else:
        print("Algoritmo no válido.")
        return None

def descifrar(algoritmo, texto_cifrado):
    if algoritmo == 'RSA':
        try:
            with open("priv_key.pem", "rb") as f:
                priv_key = RSA.import_key(f.read())
            cipher_rsa = PKCS1_OAEP.new(priv_key)
            plaintext = cipher_rsa.decrypt(texto_cifrado)
            return plaintext.decode()
        except FileNotFoundError:
            print("No se encontró la clave privada RSA. Cree la clave primero.")
            return None
    elif algoritmo == 'AES':
        try:
            with open("aes_key.bin", "rb") as f:
                key = f.read()
            cipher_aes = AES.new(key, AES.MODE_EAX)
            plaintext = cipher_aes.decrypt(texto_cifrado)
            return plaintext.decode()
        except FileNotFoundError:
            print("No se encontró la clave AES. Cree la clave primero.")
            return None
    else:
        print("Algoritmo no válido.")
        return None

# Ejemplo de uso:
#crear_clave('RSA', 2048)
#cifrado = cifrar_texto('RSA', 'Hola, mundo!')
#print("Texto cifrado:", cifrado)
#descifrado = descifrar_texto('RSA', cifrado)
#print("Texto descifrado:", descifrado)