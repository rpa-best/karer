import { defineStore } from "pinia";

interface LoaderStore {
    logo: string
    loading: boolean
}   

export default defineStore("loader", {
    state: (): LoaderStore => ({
        logo: '/favicon.ico',
        loading: true
    }),
    actions: {
        set_loading(value: boolean) {
            this.loading = value
        }
    }
})