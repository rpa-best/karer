import { defineStore } from 'pinia'
import {useToken} from "@/composables";

export const useUser = defineStore("user", {
    state: () => ({
        user: null,
        careers: [
            {
                id: 1,
                name: 'Career 1'
            },
            {
                id: 2,
                name: 'Career 2'
            }
        ],
    }),
    actions: {
        hasToken() {
            return useToken.value.access
        },
        set_career(value) {
            useToken.value.career = value
        },
        async auth(email, password) {
            useToken.value.access = email
            useToken.value.refresh = password
            await this.fetch_user()
        },
        async fetch_user() {
            if (this.user == null) {
                this.user = {
                    email: "khtkarimzhonov@gmail.com",
                    role: "manager"
                }
            }
            return this.user
        }
    }
})
