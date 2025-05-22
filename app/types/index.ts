import type { LucideIcon } from "lucide-vue-next"
import type { MenuItem } from "primevue/menuitem"

export interface DefaultQueryParams {
    limit?: number
    offset?: number
    search?: string
    ordering?: string
}

export interface SidebarItem extends MenuItem {
    licon: LucideIcon
}