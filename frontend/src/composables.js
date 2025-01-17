import { useStorage } from '@vueuse/core'

export const useToken = useStorage("token", {access: null, refresh: null, career: null})
