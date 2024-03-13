# Minimal keycloak authentication example with Nuxt 3 and Keycloak

The idea here is to have a minimal working example of an authentication system in Nuxt 3 and a python backend using Keycloak. It consists of four services: a Nuxt 3 front-end, keycloak, keycloak postgres database, a Python backend. The front-end is a Nuxt 3 project, the backend is a python Litestar app. A call to a protected dummy backend API looks like this, before and after authentication:

https://github.com/GhentCDH/nuxt-keycloak-jwt-auth/assets/60453/68997269-4494-4892-9aed-a47d72676ca2

The setup is 

## Why

Modern services in an academic or enterprise context always need some kind of authentication and authorization. However you do not want to spend much time building a custom integration with LDAP, or other authentication providers, and, most likely, you do not want to build flows for login, forgetting passwords, profile updates and so forth. Especially if these flows 

Keycloak is able to either validate users immediately or pass through validation to other authentication providers like LDAP, GitHub, OAuth accounts, ...

Once configured, Keycloak is a flexible authentication system and ties into e.g. enterprise accounts (LDAP) but has the option to add other authentication systems as well. It avoids the need to setup application-specific user management systems and flows like 'forget password', 'verify email',  'two factor authentication' are not part of your application itself but are provided by Keycloak.

## Running the example with Docker compose


Docker and some startup scripts do most of the heavy lifting. For the back-end a docker container with Python dependencies is configured. For the front-end, a Nuxt installation is done. The docker compose file also includes Keycloak istself and a PostgreSQL database container. The `.env` files in each folder contain the configuration settings for the each container. 

To make sure the hosts are accessible via a unique host name, configure `/etc/hosts` to include: 

````
127.0.0.1   keycloakkeycloak
127.0.0.1   keycloak_frontend
127.0.0.1   keycloak_backend
127.0.0.1   keycloak_example
`````

To start clone the repository and start the containers use the following docker command:

````
clone https://github.com/GhentCDH/nuxt-keycloak-jwt-auth
cd nuxt-keycloak-jwt-auth
docker compose -f compose.dev.yaml --dry-run up
open http://localhost:3000
````

After starting keycloak for the first time you also need to configure it, see below.

### Nuxt Front-end 

The front-end is build on Nuxt 3 and authentication is done with [Sidebase nuxt-auth](https://sidebase.io/nuxt-auth/getting-started). The nuxt config includes the `@sidebase/nuxt-auth` package. 

The front-end does include a server component which handles callbacks after authentication.

### Python back-end

[Litestar](https://litestar.dev/) and JWT middleware to check headers for authentication info. The `python-keycloak` package is used to interact with the keycloak instance. Now it only fetches a public key to validate JWT tokens, but integrating the package allows access to the full Keycloak API.

### PostgreSQL database

Uses a default PostgreSQL 16 docker image and the `.env` file provides a username and password.

### Keycloak project setup

Start the docker container with keycloak. The admin username and password are set via an environment variable.

In development environment 

After login, create a new @realm@. Name it myrealm

https://www.keycloak.org/server/all-config

In the new realm, a new client needs to be created with a certain client id an client secret.

* Name it `nuxt-auth`. Set the root URL to the Nuxt frontend url `http://localhost:3000/`, the home url to `http://localhost:3000/*` and the valid redirect URIs to `http://localhost:3000/*`
* Copy the Client Secret in the Credentials page. It should look similar to `65UdvUDnVEDMU1iFSNjgxH2kX1xLJa0A`. This info should end up in the `frontend/.env` file. 
* Add a user and choose a username and add a password in the credentials tab.
* Optionally add an external identity provider (such as GitHub).
* Make sure that `Client authentication`is set to OFF


## Credits

GhentCDH
