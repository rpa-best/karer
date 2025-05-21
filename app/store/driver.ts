import { defineStore } from "pinia";
import type { Driver } from "~/types/driver";


export interface DriverParams {
    search: string | null
}


interface DriverStore {
    drivers: Driver[] | undefined
}

export const useDriver = defineStore("driver", {
    state: (): DriverStore => ({
        drivers: undefined
    }),
    actions: {
        async fetchDrivers (params: DriverParams | null = null) {
            const {$api} = useNuxtApp()
            const response = await $api.get('/driver/', {params})
            this.drivers = response?.data
        },
        async createDriver(driver: Driver | FormData){
            const {$api} = useNuxtApp()
            const response = await $api.post('/driver/', driver)
            return response?.data
        },
        async updateDriver(driver_id: number, driver: Driver | FormData){
            const {$api} = useNuxtApp()
            const response = await $api.patch(`/driver/${driver_id}/`, driver)
            return response?.data
        }
    }
})