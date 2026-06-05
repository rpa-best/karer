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
            token.value = r
        },
        logout() {
            token.value.access = null
            token.value.refresh = null
            const localePath = useLocalePath()
            navigateTo(localePath('/login'))
        },
        login() {
            navigateTo(this.loginUrl())
        },
        loginUrl() {
            const localePath = useLocalePath()
            const next = useRoute().fullPath || '/'
            return `${localePath('/login')}?next=${encodeURIComponent(next)}`
        },
        isAuth() {
            return this.user?.id
        },
        redirect() {
            const rawNext = String(useRoute().query.next ?? '/')
            const next = decodeURIComponent(rawNext)
            navigateTo(next.startsWith('/') ? next : '/')
        },
    }
})