// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@sidebase/nuxt-auth'],
  devtools: { enabled: true },
  routeRules: {
    '/schema/**': { proxy: 'http://localhost:7072/schema/**' },
    '/litestar/**': { proxy: 'http://localhost:7072/litestar/**' }
  },
})
