import { defineStore } from "pinia";
import type { Invoice, Order, OrderForm, DriverComment } from "~/types/invoices";
import type { Nomenclature } from "~/types/onec";


export interface InvoiceParams {
    limit: number
    offset: number | null
    search: string | null
    status: string | null
    type: string | null
    org: string | null
    specification: string | null
    ordering: string | null
}

interface Pivot {   
    current_summa: number
    results: Nomenclature[]
    summa: number
    
}

interface InvoiceStore {
    invoices: {count: number, results: Invoice[]} | null
    pivot: Pivot | null
}

export const useInvoice = defineStore("invoice", {
    state: (): InvoiceStore => ({
        invoices: null,
        pivot: null
    }),
    actions: {
        async fetchInvoices(params: InvoiceParams) {
            const {$api} = useNuxtApp()
            const response = await $api.get('/invoice/', {params})
            this.invoices = response?.data
        },
        async createInvoice(values: Invoice) {
            const {$api} = useNuxtApp()
            return await $api.post('/invoice/', values)
        },
        async updateInvoice(pk: number, values: Invoice) {
            const {$api} = useNuxtApp()
            return await $api.patch(`/invoice/${pk}/`, values)
        },
        async fetchPivot(invoice_id: number, params: OrderParams | null = null) {
            const {$api} = useNuxtApp()
            return await $api.get(`/invoice/${invoice_id}/pivot/`, {params})
        }
    }
})


interface OrderStore {
    orders: Order[] | null
    driver_comments: DriverComment[] | null
}

export interface OrderParams {
    limit: number | null
    offset: number | null
    search: string | null
    order: string | null
}

export const useOrder = defineStore("order", {
    state: (): OrderStore => ({
        orders: null,
        driver_comments: null
    }),
    actions: {
        async fetchOrders(invoice_id: number, params: OrderParams | null = null) {
            const {$api} = useNuxtApp()
            const response = await $api.get(`/invoice/${invoice_id}/order/`, {params})
            this.orders = response?.data
        },
        async sendCareer(invoice_id: number, order_id: string) {
            const {$api} = useNuxtApp()
            return await $api.post(`/invoice/${invoice_id}/order/${order_id}/send-career/`, {}, {})
        },
        async createOrder(invoice_id: number, values: OrderForm) {
            const {$api} = useNuxtApp()
            return await $api.post(`/invoice/${invoice_id}/order/`, values)
        },
        async deleteOrder(invoice_id: number, order_id: string) {
            const {$api} = useNuxtApp()
            return await $api.delete(`/invoice/${invoice_id}/order/${order_id}/`)
        },
        async updateOrder(invoice_id: number, order_id: string, values: OrderForm) {
            const {$api} = useNuxtApp()
            return await $api.patch(`/invoice/${invoice_id}/order/${order_id}/`, values)
        },
        async fetchDriverComments(invoice_id: number, order_id: string) {
            const {$api} = useNuxtApp()
            const response = await $api.get(`/invoice/${invoice_id}/order/${order_id}/driver-comment/`)
            this.driver_comments = response?.data
        },
        async createDriverComment(invoice_id: number, order_id: string, text: string) {
            const {$api} = useNuxtApp()
            return await $api.post(`/invoice/${invoice_id}/order/${order_id}/driver-comment/`, {
                text
            })
        },
        async updateDriverComment(invoice_id: number, order_id: string, comment_id: number, text: string) {
            const {$api} = useNuxtApp()
            return await $api.patch(`/invoice/${invoice_id}/order/${order_id}/driver-comment/${comment_id}/`, {
                text
            })
        }
    }
})