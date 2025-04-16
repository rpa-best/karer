import {
    BookText, Truck, Users
  } from 'lucide-vue-next' 
import {isManager, isLogist} from "~/permissions";


export default () => {
    const sidebar = []

    if (isManager() || isLogist()) {
        sidebar.push({
            title: 'Заявки',
            url: '/',
            icon: BookText,
        })
    }

    if (isLogist()) {
        sidebar.push({
            title: 'Водители',
            url: '/driver',
            icon: Users,
        }, {
            title: 'Автомобили',
            url: '/car',
            icon: Truck,
        })
    }
    return sidebar
}
