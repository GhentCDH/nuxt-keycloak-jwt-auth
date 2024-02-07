from jose import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

unencrypted_pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()

)

pem_public_key = private_key.public_key().public_bytes(
  encoding=serialization.Encoding.PEM,
  format=serialization.PublicFormat.SubjectPublicKeyInfo
)

private_key_file = open("rk_auth_private.pem", "w")
private_key_file.write(unencrypted_pem_private_key.decode())
private_key_file.close()

public_key_file = open("rk_auth_public.pub", "w")
public_key_file.write(pem_public_key.decode())
public_key_file.close()

private_key_from_file = open("rk_auth_private.pem", "r").read().encode()

public_key_from_file = open("rk_auth_public.pub", "r").read().encode()

# print(private_key_from_file)

## OPTIONAL: public key from private key
# from cryptography.hazmat.primitives.serialization import load_pem_private_key
# pem_public_key_from_file = load_pem_private_key(private_key_from_file, password=None).public_key()

print(public_key_from_file)


token = jwt.encode({"a":"b"}, private_key_from_file, algorithm='RS256')
decoded_token = jwt.decode(token, public_key_from_file, algorithms=['RS256'])
print(decoded_token)