import { useStorage } from '@vueuse/core'

export const token = useStorage('token', { access: null, refresh: null })