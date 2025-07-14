import { useQuery } from "@tanstack/vue-query"
import { SpecificationService } from "~/services"
import type { Specification } from "~/types/onec"


export const useSpecification = (uuid: string) => {
    const service = new SpecificationService()
    return useQuery({
        queryKey: ['onec_specification', uuid],
        queryFn: async () => await service.get<Specification>(uuid)
    })
}