<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Главная',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    {
        label: 'Карер',
        items: [
            { label: 'Заявки', icon: 'pi pi-fw pi-book', to: '/invite' },
            { label: 'Водители', icon: 'pi pi-fw pi-users', to: '/driver' },
            { label: 'Автомобили', icon: 'pi pi-fw pi-truck', to: '/car' },
        ]
    },
]);
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
