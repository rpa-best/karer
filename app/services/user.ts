import type { Api } from "~/plugins/03.axios";
import type { Token, User, UserLogin } from "~/types/user";

export class UserService {
    protected readonly $api: Api;

    constructor() {
        this.$api = useNuxtApp().$api
    }
    
    async me() {
        const response = await this.$api.get<User>("/oauth/me/", {}, false)
        return response.data
    }

    async auth(values: UserLogin) {
        const response = await this.$api.post<UserLogin, Token>("/oauth/auth/", values, {}, false)
        return response.data
    }
}