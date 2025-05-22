import { ReadOnlyService } from "./utils";


export class NotificationService extends ReadOnlyService {
    constructor() {
        super('/notification/')
    }

    async read(pk: number) {
        return await this.$api.patch(`/notification/${pk}/`, {}, {}, false)
    }

    async readAll() {
        return await this.$api.patch(`/notification/read/`, {}, {}, false)
    }
}

