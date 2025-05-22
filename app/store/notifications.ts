import { defineStore } from "pinia";
import type { Notification } from "~/types/notifications";
import { NotificationService } from "~/services/notification";
import type { DefaultQueryParams } from "~/types";

interface NotificationStore {
    service: NotificationService
    items: { results?: Notification[], count?: number, unread?: number }
}

export const useNotification = defineStore("notification", {
    state: (): NotificationStore => ({
        service: new NotificationService(),
        items: {
            results: [], count: 20, unread: 0,
        }
    }),
    actions: {
        async fetchData(params: DefaultQueryParams) {
            const data = await this.service.list(params) 
            this.items = data as {results?: Notification[], count?: number, unread?: number}
        },
        async read(pk: number) {
            await this.service.read(pk)
        },
        async readAll() {
            await this.service.readAll()
        }
    }
})