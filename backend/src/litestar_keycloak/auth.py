
from keycloak import KeycloakOpenID
from decouple import config #alternative to dotenv

def get_keycloak_openid():
    server_url = config('KEYCLOAK_SERVER_URL') #"http://localhost:8080/auth/"
    client_id = config('KEYCLOAK_CLIENT_ID')
    realm_name = config('KEYCLOAK_REALM')
    client_secret_key = config('KEYCLOAK_CLIENT_SECRET')

    print("server_url ", server_url)
    print("client_id ", client_id)
    print("realm_name ", realm_name)
    print("client_secret_key ", client_secret_key) 

    return KeycloakOpenID(server_url=server_url,
                          client_id=client_id,
                          realm_name=realm_name,
                          client_secret_key=client_secret_key)




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

    #verify token
    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + get_keycloak_openid().public_key() + "\n-----END PUBLIC KEY-----\n"
    print("KEYCLOAK_PUBLIC_KEY ", get_keycloak_openid().public_key() )

    # options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
    # token_info = keycloak_openid.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)

    # print("Token info ", token_info)


    return token



