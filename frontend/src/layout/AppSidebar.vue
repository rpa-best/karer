<script>
import AppMenu from './AppMenu.vue';

export  default  {
    name: 'AppSidebar',
    components: {AppMenu},
    methods: {
        logout() {
            this.$router.push({name: 'login'})
        }
    }
}

</script>

<template>
    <div class="layout-sidebar" style="display: flex; flex-direction: column; justify-content: space-between">
        <app-menu></app-menu>
        <Button label="Выйти" variant="text" icon="pi pi-sign-out" @click="logout"/>
    </div>
</template>

<style lang="scss" scoped></style>
