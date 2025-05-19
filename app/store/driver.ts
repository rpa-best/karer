import { defineStore } from "pinia";


export interface DriverParams {
    search: string
}

export const useDriver = defineStore("driver", () => {
    const {$api} = useNuxtApp()

    const drivers = ref([])

    const fetchDrivers = async (params: DriverParams) => {
        const response = await $api.get('/driver/', {params})
        drivers.value = response?.data
    }

    return {drivers, fetchDrivers}
})