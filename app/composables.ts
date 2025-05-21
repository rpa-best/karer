import { useStorage } from '@vueuse/core'

export const token = useStorage<{ access: string | null, refresh: string | null }>(
    'token', { access: null, refresh: null }
)

export const order_columns = useStorage<string[]>(
    'order_columns', ['order']
)
