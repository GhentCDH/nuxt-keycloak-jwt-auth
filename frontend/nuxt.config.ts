// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@sidebase/nuxt-auth'],
  devtools: { enabled: true },
  ssr: true,
  auth: {
    //baseURL: 'http://localhost:9000/api/auth',
    provider: {
      type: 'authjs'
    }
  },
  routeRules: {
    '/schema/**': { proxy: 'http://localhost:7072/schema/**' },
    '/litestar/**': { proxy: 'http://localhost:7072/litestar/**' }
  },
})
