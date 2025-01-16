<script>
import AppMenuItem from './AppMenuItem.vue';
import {useUser} from "@/store";

export default {
    name: 'AppMenu',
    components: {AppMenuItem},
    data() {
        return {
            model: [
                {
                    label: 'Главная',
                    items: [{label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/'}]
                },
                {
                    label: 'Карер',
                    items: [
                        {label: 'Заявки', icon: 'pi pi-fw pi-book', to: '/invite'}
                    ]
                },
            ]
        }
    },
    async mounted() {
        if (useUser().user.role === "logist") {
            this.model[1].items.push(
                {label: 'Водители', icon: 'pi pi-fw pi-users', to: '/driver'},
                {label: 'Автомобили', icon: 'pi pi-fw pi-truck', to: '/car'},
            )
        }
    },
}
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
