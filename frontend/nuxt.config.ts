// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@sidebase/nuxt-auth'],
  devtools: { enabled: true },
  ssr: false,
  auth: {
    baseURL: 'http://localhost:9000/api/auth',
    provider: {
      type: 'authjs'
    }
  },

})
