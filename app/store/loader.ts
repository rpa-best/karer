import { defineStore } from "pinia";


export default defineStore("loader", {
    state: () => ({
        logo: '/favicon.ico',
        loading: true
    }),
    actions: {
        set_loading(value: boolean) {
            this.loading = value
        }
    }
})