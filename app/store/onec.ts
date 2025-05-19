import { defineStore } from "pinia";


export const useOrganization = defineStore("organization", () => {
    const {$api} = useNuxtApp()

    const orgs = ref([])

    const fetchOrganizations = async (params) => {
        const response = await $api.get('/onec/organization/', {params})
        orgs.value = response?.data
    }

    return {orgs, fetchOrganizations}
})

export const useSpecifications = defineStore("specifications", () => {
    const {$api} = useNuxtApp()

    const specifications = ref([])

    const fetchSpecifications = async (params) => {
        const response = await $api.get('/onec/specification/', {params})
        specifications.value = response?.data
    }

    return {specifications, fetchSpecifications}
})

export const useNomenclatures = defineStore("nomenclatures", () => {
    const {$api} = useNuxtApp()

    const nomenclatures = ref([])

    const fetchNomenclatures = async (params) => {
        const response = await $api.get('/onec/nomenclature/', {params})
        nomenclatures.value = response?.data
    }

    return {nomenclatures, fetchNomenclatures}
})