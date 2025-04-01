import axios, { type AxiosResponse, type AxiosRequestConfig, type AxiosError } from "axios";
import { token } from "~/composables";
import { useUser } from "~/store/user";

export default defineNuxtPlugin((nuxtApp) => {
  const {
    public: { NUXT_APP_BACKEND_HOST },
  } = useRuntimeConfig();

  const api = axios.create({
    baseURL: NUXT_APP_BACKEND_HOST,
  });

  const request = async (
    method: string,
    url: string,
    data: any | null,
    config: AxiosRequestConfig = {},
    toasted: boolean = true,
    redirect: boolean = true
  ): Promise<AxiosResponse | undefined> => {
    config.url = url;
    config.method = method;
    config.data = data;
    config.headers = {
      Authorization: `Bearer ${token.value.access}`,
    }
    const toast = nuxtApp.vueApp.config.globalProperties.$toast
    try {
      const response = await api.request(config);
      if (toasted) {
        toast.add({severity: 'success', summary: "Операция выполнена успешно", life: 2000})
      }
      return response
    } catch (e: unknown) {
      const error = e as AxiosError
      if (error.response?.status == 401) {
        if (token.value.refresh) {
          const { data } = await api.post("/oauth/refresh/", {
            refresh: token.value.refresh,
          });
          token.value = data
          return await request(method, url, config.data, config, toasted, redirect)
        }
        if (redirect) {
          useUser().login()
          return
        }
      }
      if (toasted) {
        const message = Object.values(error.response?.data ?? {}).map(v => typeof v === 'string' ? v : v.join('. ')).join('. ')
        toast.add({severity: 'error', summary: message, life: 2000})
      }
      throw e
    }
  };

  return {
    provide: {
      api: {
        get: async (url: string, config: AxiosRequestConfig = {}, redirect: boolean=true) => await request('get', url, null, config, false, redirect),
        post: async (url: string, data: any, config: AxiosRequestConfig = {}, toasted=true) => await request('post', url, data, config, toasted, true),
        patch: async (url: string, data: any, config: AxiosRequestConfig = {}, toasted=true) => await request('patch', url, data, config, toasted, true),
        delete: async (url: string, config: AxiosRequestConfig = {}, toasted=true) => await request('delete', url, null, config, toasted, true),
      }
    },
  };
})
