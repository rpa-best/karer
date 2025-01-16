import { defineStore } from 'pinia'

export const useUser = defineStore("user", {
    state: () => ({
        user: null
    }),
    actions: {
        async fetch_user() {
            if (this.user == null) {
                this.user = {
                    role: "logist"
                }
            }
            return this.user
        }
    }
})
