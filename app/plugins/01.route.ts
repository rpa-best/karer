import loader from "~/store/loader";

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.$router.beforeEach((to, from) => {
    if (to.path !== from.path) {
      loader().set_loading(true)
    }
  });
  nuxtApp.$router.afterEach(() => {
    setTimeout(() => loader().set_loading(false), 100)
  });
});
