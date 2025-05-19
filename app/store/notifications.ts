import { defineStore } from "pinia";


export interface Notification {
    id: number,
    label: string
    message: string
    redirect_url: string
    read: boolean
    created_at: string
    read_at: string
    severity: string
}


interface NotificationStore {
    items: { results: Notification[], count: number, unread: number }
}


export const useNotification = defineStore("notification", {
    state: (): NotificationStore => ({
        items: {
            results: [], count: 20, unread: 0,
        }
    }),
    actions: {
        async fetchData() {
            const {$api} = useNuxtApp()
            const response = await $api.get('/notification/', { params: { limit: 30 } })
            this.items = response?.data
        },
        async read(pk: number) {
            const {$api} = useNuxtApp()
            await $api.patch(`/notification/${pk}/`, {}, {}, false)
        },
        async readAll() {
            const {$api} = useNuxtApp()
            await $api.patch(`/notification/read/`, {}, {}, false)
        }
    }
})