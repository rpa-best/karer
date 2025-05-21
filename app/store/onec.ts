import { defineStore } from "pinia";
import type { Nomenclature, Organization, Specification } from "~/types/onec";

interface OrganizationStore {
    organizations: Organization[] | undefined
}

interface OrganizationParams {
    limit: number
    offset: number
    search: string
    ordering: string
}

export const useOrganization = defineStore("organization", {
    state: (): OrganizationStore => ({
        organizations: undefined
    }),
    actions: {
        async fetchOrganizations(params: OrganizationParams | null = null) {
            const {$api} = useNuxtApp()

            const response = await $api.get('/onec/organization/', {params})
            this.organizations = response?.data
        }
    }
})

interface SpecificationStore {
    specifications: Specification[] | undefined
}

interface SpecificationParams {
    limit: number
    offset: number
    search: string
    ordering: string
}

export const useSpecification = defineStore("specification", {
    state: (): SpecificationStore => ({
        specifications: undefined
    }),
    actions: {
        async fetchSpecifications(params: SpecificationParams | null = null) {
            const {$api} = useNuxtApp()

            const response = await $api.get('/onec/specification/', {params})
            this.specifications = response?.data
        }
    }
})


interface NomenclatureStore {
    nomenclatures: Nomenclature[] | undefined
}

interface NomenclatureParams {
    limit: number
    offset: number
    search: string
    ordering: string
}

export const useNomenclature = defineStore("nomenclature", {
    state: (): NomenclatureStore => ({
        nomenclatures: undefined
    }),
    actions: {
        async fetchNomenclatures(params: NomenclatureParams | null = null) {
            const {$api} = useNuxtApp()

            const response = await $api.get('/onec/nomenclature/', {params})
            this.nomenclatures = response?.data
        }
    }
})