import {useUser} from "@/store";

export const check_permissions = async (to, from, next) => {
    if (to.meta && to.meta.permissions) {
        for (let func of to.meta.permissions) {
            if (!func({to, from, next})) {
                return false
            }
        }
    }
    return true
}

export const isAuth = async () => {
    return useUser().user.id
}

export const isLogist = () => {
    return useUser().user.role === "logist"
}

export const isManager = () => {
    return useUser().user.role === "manager"
}
