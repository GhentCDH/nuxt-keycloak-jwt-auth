from typing import Optional
from litestar import Litestar, get, Request
from litestar.connection import ASGIConnection
from litestar.security.jwt import JWTAuth, Token
import json

from .auth import login_with_username_password

#https://docs.litestar.dev/2/reference/security/jwt.html#litestar.security.jwt.JWTAuthenticationMiddleware


@get("/litestar/public")
async def public() -> str:
    return "Public information! Index"

@get("/litestar/protected")
async def protected(request: "Request[User, Token, Any]") -> str:
    assert isinstance(request.user, User)
    # request.auth is the instance of 'litestar_jwt.Token' created from the data encoded in the auth header
    assert isinstance(request.auth, Token)
    token_info = json.dumps(request.auth.extras, indent=4, sort_keys=True)
    return "Protected information! Authentication token info: " + token_info

@get("/litestar/jwt_token") 
async def jwt_token() -> str:
    username = "ghentcdh"
    password = "ghentcdh"
    token = login_with_username_password(username, password)
    return json.dumps(token, indent=4, sort_keys=True)

class User():
    id: int
    name: str
    email: str
    roles: list[str]

    def __init__(self, id: int, name: str, email: str, roles: list[str]):
        self.id = id
        self.name = name
        self.email = email
        self.roles = roles
    

# See https://docs.litestar.dev/2/usage/security/jwt.html


async def retrieve_user_handler(token: "Token", connection: "ASGIConnection[Any, Any, Any, Any]") -> User:
    """
    Retrieve user handler.

    Args:
        token (Token): The decoded JWT token with user info.
        connection (ASGIConnection[Any, Any, Any, Any]): The ASGI connection.

    Returns:
        Optional[User]: The user instance if found, otherwise None.
    """
    # logic here to retrieve the user instance
    email = token.extras["email"]
    name = token.extras["name"]
    roles = token.extras["realm_access"]["roles"]
    user =User(1, name, email,roles)
    return user

# app = Litestar([index,auth],middleware=[DefineMiddleware(JWTAuthMiddleware)])
# app = Litestar([index,auth],middleware=[JWTAuthenticationMiddleware()])

rsa_pub = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAua/OCq5mN0yZsnL0fiPHDB/dIxmGE7ME/HGy36R+KttOpb04+krV+rb2hZHFUAxtZnr/ViTcb0cgOjE6Xrpt4yPHIWZlJo871mlWxRcUvm2GcmsoVuC6tvEfdAnt0pOfQ886owf5PppYf7k/u+mZcnoW7BIwJGUkegOPOFfmXVhuVgp679kqz7Q06EWHpVpkpZgdFiPky7c+IatqPJbUNUrdlhOPmDHvA5Rkpeb6T764tXnIBq1pt4IXkcz5iTUwir8NkNmmFVPI4iEubFwUAh/rXhbGPGo0S4fqm4TaI61SvHZ9GV6NYzbmQ/2LY9WXkBdrtCt1Z7416FBU6FKRhQIDAQAB"
rsa_pub = f"-----BEGIN PUBLIC KEY-----\n{rsa_pub}\n-----END PUBLIC KEY-----\n"
secret = rsa_pub

jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=secret,
    auth_header="authorization",
    algorithm="RS256",
    # we are specifying which endpoints should be excluded from authentication. In this case the login endpoint
    # and our openAPI docs.
    exclude=["/litestar/public", "/schema","/litestar/jwt_token"],
)

app = Litestar([public,protected,jwt_token], on_app_init=[jwt_auth.on_app_init])
