import { useStorage } from '@vueuse/core'
import type { Token } from '~/types/user'

export const token = useStorage<Token>(
    'token', { access: null, refresh: null }
)

export const order_columns = useStorage<string[]>(
    'order_columns', ['order']
)
