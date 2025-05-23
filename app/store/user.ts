import { defineStore } from "pinia";
import { token } from "~/composables";
import { UserService } from "~/services/user";
import type { User } from "~/types/user";
import type { UserLogin } from "~/types/user";

interface UserStore {
    user: User | undefined
}

export const useUser = defineStore("user", {
    state: (): UserStore => ({
        user: undefined
    }),
    actions: {
        async auth(values: UserLogin) {
            const user_service = new UserService()
            const r = await user_service.auth(values)
            token.value = r?.data
        },
        logout() {
            token.value.access = null
            token.value.refresh = null
            navigateTo('/login')
        },
        login() {
            navigateTo(this.loginUrl())
        },
        loginUrl() {
            return `/login?next=${useRequestURL().href}`
        },
        isAuth() {
            return this.user?.id
        },
        redirect() {
            navigateTo(String(useRoute().query.next ?? '/'))
        },
    }
})