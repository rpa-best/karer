import { useQuery } from "@tanstack/vue-query"
import { OrganizationService } from "~/services"
import type { Organization } from "~/types/onec"


export const useOrganization = (uuid: string) => {
    const service = new OrganizationService()
    return useQuery({
        queryKey: ['onec_organization', uuid],
        queryFn: async () => await service.get<Organization>(uuid)
    })
}