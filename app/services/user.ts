import type { Api } from "~/plugins/03.axios";
import type { Token, User, UserLogin } from "~/types/user";

export class UserService {
    protected readonly $api: Api;

    constructor() {
        this.$api = useNuxtApp().$api
    }
    
    me() {
        return this.$api.get<User>("/oauth/me/", {}, false)
    }

    auth(values: UserLogin) {
        return this.$api.post<UserLogin, Token>("/oauth/auth/", values, {}, false)
    }
}