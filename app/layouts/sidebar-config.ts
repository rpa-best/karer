import {isManager, isLogist} from "~/permissions";
import { BookText, Users, Truck } from "lucide-vue-next";
import type { SidebarItem } from '~/types';


export default (): SidebarItem[] => {
    const sidebar: SidebarItem[] = []

    if (isManager() || isLogist()) {
        sidebar.push({
            title: 'Заявки',
            url: '/',
            licon: BookText,
        })
    }

    if (isLogist()) {
        sidebar.push({
            title: 'Водители',
            url: '/driver',
            licon: Users,
        }, {
            title: 'Автомобили',
            url: '/car',
            licon: Truck,
        })
    }
    return sidebar
}
