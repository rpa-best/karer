import { defineStore } from "pinia";
import { token } from "~/composables";
import type { User } from "~/types/user";
import type { UserLogin } from "~/types/user";

interface UserStore {
    user: User | null
}

export const useUser = defineStore("user", {
    state: (): UserStore => ({
        user: null
    }),
    actions: {
        async fetch_user() {
            const { $api } = useNuxtApp()
            const r = await $api.get("/oauth/me/", {}, false)
            this.user = r?.data
        },
        async auth(values: UserLogin) {
            const { $api } = useNuxtApp()
            const r = await $api.post("/oauth/auth/", values, {}, false)
            token.value = r?.data
        },
        logout() {
            token.value.access = null
            token.value.refresh = null
            window.location.href = '/login'
        },
        login() {
            window.location.href = this.loginUrl()
        },
        loginUrl() {
            return `/login?next=${useRequestURL().href}`
        },
        isAuth() {
            return this.user?.id
        },
        redirect() {
            window.location.href = String(useRoute().query.next ?? '/')
        },
    }
})