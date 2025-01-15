<script setup>
import AppMenu from './AppMenu.vue';
</script>

<template>
    <div class="layout-sidebar" style="display: flex; flex-direction: column; justify-content: space-between">
        <app-menu></app-menu>
        <Button label="Выйти" variant="text" icon="pi pi-sign-out" />
    </div>
</template>

<style lang="scss" scoped></style>
