import { token } from "~/composables";
import { useUser } from "~/store/user";

export default defineNuxtRouteMiddleware((to, from) => {
  // isAuthenticated() is an example method verifying if a user is authenticated
  if (token.value.access) {
    useUser().login()
    return
  }
});
