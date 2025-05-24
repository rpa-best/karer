import { ReadOnlyService } from "./utils";


export class NotificationService extends ReadOnlyService {
    constructor() {
        super('/notification/')
    }

    async read(pk: number) {
        const response = await this.$api.patch(`/notification/${pk}/`, {}, {}, false)
        return response.data
    }

    async readAll() {
        const response = await this.$api.patch(`/notification/read/`, {}, {}, false)
        return response.data
    }
}

