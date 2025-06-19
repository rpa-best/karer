import type { InvoiceParams } from "~/types/invoices";
import { CRUDService, ReadOnlyService } from "./utils";


class DriverCommentService extends CRUDService {
    constructor() {
        super('/invoice/{invoice_id}/order/{order_id}/driver-comment/')
    }
}


class OrderService extends CRUDService {
    driverComment: DriverCommentService
    constructor() {
        super('/invoice/{invoice_id}/order/')
        this.driverComment = new DriverCommentService()
    }

    async sendCareer(invoice_id: number, order_id: string) {
        const response = await this.$api.post(`/invoice/${invoice_id}/order/${order_id}/send_career/`, {}, {})
        return response.data
    }
}


class AvailableNomenclatureService extends ReadOnlyService {
    constructor() {
        super('/invoice/{invoice_id}/available_nomenclature/')
    }
}


export class InvoiceService extends CRUDService {
    order = new OrderService()
    nomenclature = new AvailableNomenclatureService()
    
    constructor() {
        super('/invoice/')
    }

    async fetchPivot<T = any>(invoice_id: number, params: InvoiceParams | null = null): Promise<T> {
        const response = await this.$api.get<T>(`/invoice/${invoice_id}/pivot/`, {params})
        return response.data
    }
}
