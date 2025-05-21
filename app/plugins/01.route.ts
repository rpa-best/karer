import loader from "~/store/loader";

export default defineNuxtPlugin((nuxtApp) => {
  const router = useRouter()
  router.beforeEach((to, from) => {
    if (to.path !== from.path) {
      loader().set_loading(true)
    }
  });
  
  router.afterEach(() => {
    setTimeout(() => loader().set_loading(false), 100)
  });
});
