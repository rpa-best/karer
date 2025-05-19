import { defineStore } from "pinia";

export const useInvoice = defineStore("invoice", {
    state: () => ({
        invoices: {
            results: [], count: 20
        }
    }),
    actions: {
        async fetchInvoices(params) {
            const {$api} = useNuxtApp()
            const response = await $api.get('/invoice/', {params})
            this.invoices = response?.data
        },
        async createInvoice(values) {
            const {$api} = useNuxtApp()
            return await $api.post('/invoice/', values)
        },
        async updateInvoice(pk, values) {
            const {$api} = useNuxtApp()
            return await $api.patch(`/invoice/${pk}/`, values)
        }
    }
})