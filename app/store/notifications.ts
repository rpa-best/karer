import { defineStore } from "pinia";
import type { Notification } from "~/types/notifications";
import { NotificationService } from "~/services/notification";
import { NotificationSocket } from "~/components/notifications/websocket";

interface NotificationStore {
    service: NotificationService
    socket: NotificationSocket
    items: { results: Notification[], count: number, unread: number }
}

export const useNotification = defineStore("notification", {
    state: (): NotificationStore => ({
        service: new NotificationService(),
        socket: new NotificationSocket(),
        items: {
            results: [],
            count: 0,
            unread: 0,
        }
    })
})