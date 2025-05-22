import {Client} from "@/components/utils"
import {useNotification} from "~/store/notifications";
import { useNuxtApp } from '#app';

export class NotificationSocket extends Client {
    severities = {
        'success': 'success',
        'info': 'info',
        'danger': 'error',
    }
    constructor() {
        const onopen = () => {
            console.log(`Websocket open: ${this.url}`);
        }

        const onclose = () => {
            console.log(`Websocket closed: ${this.url}`);
        }
        const onmessage = (r: MessageEvent) => {
            const data = JSON.parse(r.data)

            if (typeof window !== 'undefined') {
                const toast = useNuxtApp().vueApp.config.globalProperties.$toast
                const notification = useNotification()

                notification.items.results = [data, ...(notification.items.results || [])   ]
                notification.items.unread = (notification.items.unread || 0) + 1
                toast.add({
                    severity: this.severities[data.severity as keyof typeof this.severities],
                    summary: data.label,
                    detail: data.message,
                    // command: async () => {
                    //     await useRouter().push(data.redirect_url)
                    // },
                    life: 10000
                })
            }
        }
        super(`/ws/notification/`, onopen, onmessage, onclose)
    }
}