import type { Api } from "~/plugins/03.axios"
import type { DefaultQueryParams } from "~/types"

export class ReadOnlyService {
    protected readonly $api: Api
    protected readonly baseUrl: string

    constructor(baseUrl: string) {
        this.$api = useNuxtApp().$api
        this.baseUrl = baseUrl
    }

    protected getUrl(url_params: Record<string, string | number> = {}): string {
        let url = this.baseUrl
        for (const [key, value] of Object.entries(url_params)) {
            url = url.replace(`{${key}}`, `${value}`)
        }
        if (url.endsWith('/')) {
            url = url.slice(0, -1)
        }
        return url
    }

    async list<T extends object>(params: DefaultQueryParams | null = null, url_params: Record<string, string | number> = {}): Promise<T[]> {
        const response = await this.$api.get(`${this.getUrl(url_params)}/`, {params})
        return response.data
    }

    async get<T extends object>(id: number | string, params: DefaultQueryParams | null = null, url_params: Record<string, string | number> = {}): Promise<T> {
        const url = this.getUrl(url_params)
        const response = await this.$api.get(`${url}/${id}/`, {params})
        return response.data
    }
}


export class CRUDService extends ReadOnlyService {
    async create<T extends object>(data: T, params: DefaultQueryParams | null = null, url_params: Record<string, string | number> = {}): Promise<T> {
        const response = await this.$api.post(`${this.getUrl(url_params)}/`, data, {params})
        return response.data
    }

    async update<T extends object>(id: number | string, data: T, params: DefaultQueryParams | null = null, url_params: Record<string, string | number> = {}): Promise<T> {
        const url = this.getUrl(url_params)
        const response = await this.$api.patch(`${url}/${id}/`, data, {params})
        return response.data
    }

    async delete<T extends object>(id: number | string, params: DefaultQueryParams | null = null, url_params: Record<string, string | number> = {}): Promise<T> {
        const url = this.getUrl(url_params)
        const response = await this.$api.delete(`${url}/${id}/`, {params})
        return response.data
    }
}
