import {useUser} from "@/store";
import {check_permissions} from "./permissions"

export async function auth({to, next}) {
    if (!useUser().hasToken()) {
        return next(`/login?next=${to.fullPath}`)
    }
    try {
        await useUser().fetch_user()
    } catch (e) {
        console.log(e)
        return next(`/login?next=${to.fullPath}`)
    }


}

export async function permission({to, from, next}) {
    if (!useUser().user.role || !await check_permissions(to, from, next)) {
        return next(`/auth/access?next=${to.fullPath}`);
    }
}
