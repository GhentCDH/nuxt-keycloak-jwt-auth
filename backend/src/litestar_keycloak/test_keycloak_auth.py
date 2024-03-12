
import json
import requests
from auth import login_with_username_password

from jose import JWSError, JWTError, jwt

HEADER_FIELD_NAME = "Authorization"
URL_API_BASE = "http://localhost:8000"
URL_PUBLIC = f"{URL_API_BASE}/litestar/public"
URL_PROTECTED = f"{URL_API_BASE}/litestar/protected"


def send_get_request_with_header(url, auth_header_data):
    """
    Sends a GET request to the provided URL with the provided token in the
    header.

    Args:
        url (str): The URL to send the GET request to.
        token (str): The token to include in the header.

    Returns:
        str: The response from the GET request.
    """
    headers = {HEADER_FIELD_NAME: auth_header_data}
    response = requests.get(url, headers=headers)
    return response

# Expected to work, resource is public
# response = send_get_request_with_header(URL_PUBLIC, "")
# print(response.text)

# # Expected to fail, as no token is provided and resource is protected
# response = send_get_request_with_header(URL_PROTECTED, "")
# print(response.text)


# Receive login token from keycloak and use it to access protected resource:
username = "ghentcdh"
password = "ghentcdh"
token = login_with_username_password(username, password)

print("Received token from keycloak:",  json.dumps(token, indent=4, sort_keys=True))

print("access_token:", token["access_token"])

access_token = token["access_token"]

# retrieve token from http://keycloakkeycloak:8080/realms/myrealm
rsa_pub = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAua/OCq5mN0yZsnL0fiPHDB/dIxmGE7ME/HGy36R+KttOpb04+krV+rb2hZHFUAxtZnr/ViTcb0cgOjE6Xrpt4yPHIWZlJo871mlWxRcUvm2GcmsoVuC6tvEfdAnt0pOfQ886owf5PppYf7k/u+mZcnoW7BIwJGUkegOPOFfmXVhuVgp679kqz7Q06EWHpVpkpZgdFiPky7c+IatqPJbUNUrdlhOPmDHvA5Rkpeb6T764tXnIBq1pt4IXkcz5iTUwir8NkNmmFVPI4iEubFwUAh/rXhbGPGo0S4fqm4TaI61SvHZ9GV6NYzbmQ/2LY9WXkBdrtCt1Z7416FBU6FKRhQIDAQAB"
rsa_pub = f"-----BEGIN PUBLIC KEY-----\n{rsa_pub}\n-----END PUBLIC KEY-----\n"
secret = rsa_pub

unverified_header = jwt.get_unverified_header(token=access_token)
algorithm = unverified_header["alg"]
# print("unverified_header:", json.dumps(unverified_header, indent=4, sort_keys=True))

unverified_claims = jwt.get_unverified_claims(token=access_token)
# print("unverified_claims:", json.dumps(unverified_claims, indent=4, sort_keys=True))

payload = jwt.decode(token=access_token, key=secret, algorithms=[algorithm], options={"verify_aud": False})

print("verified payload:", json.dumps(payload, indent=4, sort_keys=True))

# Expected to work even if token is provided for public resource
response = send_get_request_with_header(URL_PUBLIC, f"access_token: {access_token}")

# Expected to work, as token is provided and resource is protected
response = send_get_request_with_header(URL_PROTECTED, f"access_token: {access_token}")

# username = "ghentcdh"
# password = "mypass"
# token = login_with_username_password(username, password)
# throws keycloak.exceptions.KeycloakAuthenticationError
