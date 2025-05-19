import { defineStore } from "pinia";


export interface CarsParams {
    search: string
}

export const useCar = defineStore("car", () => {
    const {$api} = useNuxtApp()

    const cars = ref([])

    const fetchCars = async (params: CarsParams) => {
        const response = await $api.get('/car/', {params})
        cars.value = response?.data
    }

    return {cars, fetchCars}
})