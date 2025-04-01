import { createPinia } from 'pinia'
import ToastService from 'primevue/toastservice';

export default defineNuxtPlugin((nuxtApp) => {
    const pinia = createPinia()
    
    nuxtApp.vueApp.use(pinia)
    nuxtApp.vueApp.use(ToastService)
})