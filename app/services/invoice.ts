import type { InvoiceParams } from "~/types/invoices";
import { CRUDService } from "./utils";


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
        return await this.$api.post(`/invoice/${invoice_id}/order/${order_id}/send_career/`, {}, {})
    }
}


export class InvoiceService extends CRUDService {
    order: OrderService
    
    constructor() {
        super('/invoice/')
        this.order = new OrderService()
    }

    async fetchPivot(invoice_id: number, params: InvoiceParams | null = null) {
        const response = await this.$api.get(`/invoice/${invoice_id}/pivot/`, {params})
        return response.data
    }
}
