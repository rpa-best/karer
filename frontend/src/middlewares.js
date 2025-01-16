import {useUser} from "@/store";
import {check_permissions} from "./permissions"

export async function auth({to, from, next}) {
    const user = await useUser().fetch_user()
    if (!user.role || !await check_permissions(to, from, next)) {
        return next(`/auth/access?next=${to.fullPath}`);
    }
}
