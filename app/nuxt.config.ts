// https://nuxt.com/docs/api/configuration/nuxt-config
import Preset from "./theme";

export default defineNuxtConfig({
  modules: [
    "@primevue/nuxt-module",
    "@nuxtjs/tailwindcss",
    "@nuxtjs/i18n",
    '@nuxtjs/leaflet',
    '@nuxtjs/color-mode',
  ],
  ssr: true,
  runtimeConfig: {
    public: {
      NUXT_APP_BACKEND_HOST: process.env.NUXT_APP_BACKEND_HOST,
      VAPID_PUBLIC_KEY: process.env.VAPID_PUBLIC_KEY,
    }
  },  
  colorMode: {
    preference: 'light',
    fallback: 'light',
  },

  primevue: {
    autoImport: true,
    options: {
      ripple: true,
      theme: Preset,
    },
  },

  i18n: {
    lazy: true,
    langDir: 'locales',
    strategy: 'prefix_except_default',
    locales: [
      { code: 'ru', language: 'ru', name: 'Русский', file: 'ru.json', cache: false },
      { code: 'uz', language: 'uz', name: 'O\'zbek', file: 'uz.json', cache: false }
    ],
    defaultLocale: 'ru'
  },

  compatibilityDate: '2025-03-19',
});