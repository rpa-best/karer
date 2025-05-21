import {Client} from "@/components/utils"
import {useNotification} from "~/store/notifications";
import { useNuxtApp } from '#app';

export class NotificationSocket extends Client {
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

                notification.items.results = [data, ...notification.items.results]
                notification.items.unread += 1

                toast.add({
                    severity: data.severity,
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