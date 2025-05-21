import { defineStore } from "pinia";
import type { Car } from "~/types/car";


export interface CarsParams {
    search?: string | null
}

interface CarStore {
    cars: Car[] | undefined
}

export const useCar = defineStore("car", {
    state: (): CarStore => ({
        cars: undefined
    }),
    actions: {
        async fetchCars(params: CarsParams | null = null){
            const {$api} = useNuxtApp()
            const response = await $api.get('/car/', {params})
            this.cars = response?.data
        },
        async createCar(car: Car | FormData){
            const {$api} = useNuxtApp()
            const response = await $api.post('/car/', car)
            return response?.data
        },
        async updateCar(car_id: number, car: Car | FormData){
            const {$api} = useNuxtApp()
            const response = await $api.patch(`/car/${car_id}/`, car)
            return response?.data
        }
    }
})