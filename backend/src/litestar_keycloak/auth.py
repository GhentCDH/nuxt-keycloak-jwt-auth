
from keycloak import KeycloakOpenID
from decouple import config #alternative to dotenv

def get_keycloak_openid():
    server_url = config('KEYCLOAK_ISSUER') #"http://localhost:8080/auth/"
    client_id = config('KEYCLOAK_CLIENT_ID')
    realm_name = config('KEYCLOAK_REALM')
    client_secret_key = config('KEYCLOAK_CLIENT_SECRET')
    
    print("Keycloak server_url ", server_url)
    print("Keycloak client_id ", client_id)
    print("Keycloak realm_name ", realm_name)
    print("Keycloak client_secret_key ", client_secret_key)

    return KeycloakOpenID(server_url=server_url,
                          client_id=client_id,
                          realm_name=realm_name,
                          client_secret_key=client_secret_key)

def get_keycloak_public_key():
    """
    Retrieves the public key from the Keycloak OpenID provider.

    Returns:
        str: The public key in PEM format.
    """
    keycloak_openid = get_keycloak_openid()
    return "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----\n"

def login_with_username_password(username, password):
    """
    Logs in a user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        str: The authentication token for the logged-in user.
    """
    keycloak_openid = get_keycloak_openid()

    # Get Token
    token = keycloak_openid.token(username, password)

    return token



