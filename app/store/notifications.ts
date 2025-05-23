import { defineStore } from "pinia";
import type { Notification } from "~/types/notifications";
import { NotificationService } from "~/services/notification";

interface NotificationStore {
    service: NotificationService
    items: { results: Notification[], count: number, unread: number }
}

export const useNotification = defineStore("notification", {
    state: (): NotificationStore => ({
        service: new NotificationService(),
        items: {
            results: [],
            count: 0,
            unread: 0,
        }
    })
})