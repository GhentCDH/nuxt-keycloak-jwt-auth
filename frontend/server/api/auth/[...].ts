// this file catches all requests to /api/auth/* and passes them to the NuxtAuthHandler

import { NuxtAuthHandler } from '#auth'

//const config = useRuntimeConfig()

// See for more info:
// https://github.com/nextauthjs/next-auth/blob/v4/packages/next-auth/src/providers/keycloak.ts

const decode = function (token) {
    //console.log(Buffer.from(token.split('.')[1], 'base64').toString())

    return JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString())
 }

// KeycloakProvider is a custom auth provider that extends the default provider
import KeycloakProvider from 'next-auth/providers/keycloak'

console.log("")

console.log("---------------------------------------")
console.log("Nuxt AUTH_ORIGIN",   process.env.AUTH_ORIGIN)
console.log("Nuxt NUXT_AUTH_SECRET", process.env.NUXT_AUTH_SECRET)
console.log("Keycloak KEYCLOAK_CLIENT_ID",process.env.KEYCLOAK_CLIENT_ID)
console.log("Keycloak KEYCLOAK_CLIENT_SECRET",process.env.KEYCLOAK_CLIENT_SECRET)
console.log("Keycloak KEYCLOAK_ISSUER", process.env.KEYCLOAK_ISSUER)
console.log("---------------------------------------")
console.log("")

export default NuxtAuthHandler({
    secret: process.env.NUXT_AUTH_SECRET,

    session: {
        strategy: "jwt", // Use JSON Web Tokens (JWT) for session management
    },
    providers: [
        // @ts-expect-error You need to use .default here for it to work during SSR. 
        // May be fixed via Vite at some point
        KeycloakProvider.default({
          clientId: process.env.KEYCLOAK_CLIENT_ID,
          clientSecret: process.env.KEYCLOAK_CLIENT_SECRET,
          issuer: process.env.KEYCLOAK_ISSUER,
           //callbackUrl: 'http://localhost:9000/api/auth/callback/keycloak',
          authorization: { params: { scope: 'openid email roles' } }
        })
    ],
    callbacks: {
        async jwt({ token, user, account, profile }) {

          console.log("Callback token:",token);console.log("")
          console.log("Callback user:",user);console.log("")
          console.log("Callback account:",account);console.log("")
          console.log("Callback profile:",profile);console.log("")

          if (account) {
            token.accessToken = account.access_token

            console.log("Callback account call:",account)
            console.log(account.access_token)

            const decodedToken = decode(account.access_token)
            const sub = decodedToken.sub
            const roles = decodedToken.realm_access.roles
            const refreshToken = account.refresh_token

            console.log(roles,sub)
            token.user = {
              ...user,
              sub,
              roles,
            }
            token.refreshToken = refreshToken
          }
          console.log("Callback token call:",token)
          return token;
        },
        async session({ session, token, user }) {

          console.log("Session token:",token)
          console.log("Session user:",user )
          console.log("Session session:",session)
          
          session.user = token.user
          session.accessToken = token.accessToken
          session.refreshToken = token.refreshToken

          return session;
        },
    }
})
