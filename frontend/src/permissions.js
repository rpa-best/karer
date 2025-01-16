import {useUser} from "@/store";

export const check_permissions = async (to, from, next) => {
    if (to.meta && to.meta.permissions) {
        for (let func of to.meta.permissions) {
            if (!await func({to, from, next})) {
                return false
            }
        }
    }
    return true
}

export const isAuth = async () => {
    const user = await useUser().fetch_user()
    return user.id
}

export const isLogist = async () => {
    const user = await useUser().fetch_user()
    return user.role === "logist"
}

export const isManager = async () => {
    const user = await useUser().fetch_user()
    return user.role === "manager"
}
