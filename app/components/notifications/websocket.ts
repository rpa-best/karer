import {Client} from "@/components/utils"
import {useNotification} from "~/store/notifications";


export class NotificationSocket extends Client {
    constructor() {
        super(`/ws/notification/`)
    }

    override onmessage(r: MessageEvent) {
        const data = JSON.parse(r.data)
        const severities = {
            'success': 'success',
            'info': 'info',
            'danger': 'error',
        }

        if (typeof window !== 'undefined') {
            const toast = useNuxtApp().vueApp.config.globalProperties.$toast
            const notification = useNotification()

            const items = notification.items
            notification.$state.items = {
                results: [data, ...items.results],
                unread: (items.unread || 0) + 1,
                count: (items.count || 0) + 1
            }

            toast.add({
                severity: severities[data.severity as keyof typeof severities],
                summary: data.label,
                detail: data.message,
                life: 5000
            })
        }
    }
}