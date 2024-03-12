# Minimal keycloak authentication example with Nuxt 3 and Keycloak

The idea here is to have a minimal working example of an authentication system in Nuxt 3 and a python backend using Keycloak. It consists of four services: a Nuxt 3 front-end, keycloak, keycloak postgres database, a Python backend. The front-end is a Nuxt 3 project, the backend is a python Litestar app.

## Why

Modern services in an academic or enterprise context always need some kind of authentication and authorization. However you do not want to spend much time building a custom integration with LDAP, or other authentication providers, and, most likely, you do not want to build flows for login, forgetting passwords, profile updates,... 

Keycloak is able to either validate users immediately or pass through validation to other authentication providers like LDAP, GitHub, OAuth accounts, ...

Once configured, Keycloak is a flexible authentication system and ties into e.g. enterprise accounts (LDAP) but has the option to add other authentication systems as well. It avoids the need to setup application-specific user management systems and flows like 'forget password', 'verify email',  'two factor authentication' are not part of your application itself but are provided by Keycloak.

alternative? https://github.com/aborn/nuxt-openid-connect

## Docker compose


pdm run  uvicorn src.litestar_keycloak.app:app --reload --port 0


## Nuxt Project setup

Make sure to install the dependencies:

To install 

```bash
pnpm i -D @sidebase/nuxt-auth
pnpm i next-auth@4.22.5
```

````
//file ./nuxt.config.tx
export default defineNuxtConfig({
  modules: ['@sidebase/nuxt-auth'],
  devtools: { enabled: true }
})
````

````
//file ./server/api/auth/[...].ts
import { NuxtAuthHandler } from '#auth'

import KeycloakProvider from 'next-auth/providers/keycloak'
export default NuxtAuthHandler({
    providers: [
        // @ts-expect-error You need to use .default here for it to work during SSR. May be fixed via Vite at some point
        KeycloakProvider.default({
           clientId: 'nuxt-auth',
           clientSecret: 'pyoq3sCc8w3t10T4GnxKA9eEchKoZ4wh',
           issuer: 'http://127.0.0.1:7766/realms/myrealm'
        })
    ]
})

````

Start the development server on `http://localhost:3000`:

```bash
# pnpm
pnpm run dev
```

## Keycloak Project setup

Start the docker container with keycloak. The admin username and password are set via an environment variable.

In development environment 

After login, create a new @realm@. Name it myrealm

https://www.keycloak.org/server/all-config


In the new realm, a new client needs to be created with a certain client id an client secret.

Name it `nuxt-auth`. Set the root URL to the Nuxt frontend url `http://localhost:3000/`, the home url to `http://localhost:3000/*` and the valid redirect URIs to `http://localhost:3000/*`

Copy the Client Secret in the Credentials page. It should look similar to `65UdvUInVEDMU1iFSNjgxH2kX1xLJa0A`

Add a user and choose a username and add a password in the credentials tab.

Optionally add an external identity provider (such as GitHub).

Make sure that `Client authentication`is set to OFF


## Credits

GhentCDH