<script>
import Driver from "./Driver.vue";

export default {
    name: 'Drivers',
    components: {Driver},
    data() {
        return {
            loading: true,
            driver: {},
            show_driver: false,
            drivers: [
                {
                    id: 1,
                    name: 'Панов Гордий Оскарович',
                    phone: '+7 (881) 791 84 48',
                    telegram: "4234325423",
                    birth_date: "18.05.1999"
                }
            ],
            filters: {
                search: null,
            }
        }
    },
    async mounted() {
        await this.fetch_data()
    },
    methods: {
        rowClick(e) {
            this.show_driver = true
            this.driver = e.data
        },
        async onFilter() {
            await this.fetch_data()
        },
        async fetch_data() {
            this.loading = true
            console.log(this.filters)
            setTimeout(() => {
                this.loading = false
            }, 3000)
        }
    }
}
</script>

<template>
    <div>
        <div class="flex justify-content-between align-items-center flex-wrap">
            <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Водители</h2>
            <div class="flex md:flex-nowrap flex-wrap md:w-auto w-full">
                <IconField class="w-full mb-3">
                    <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full"/>
                    <InputIcon>
                        <i class="pi pi-search cursor-pointer" @click="onFilter"/>
                    </InputIcon>
                </IconField>
            </div>
        </div>
        <Card>
            <template #content>
                <DataTable size="large" :value="drivers" :loading="loading" lazy @row-click="rowClick" rowHover>
                    <Column field="id" header="ID" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="name" header="ФИО" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="phone" header="Телефон" style="font-weight: 600" header-class="carsHeader"></Column>
                </DataTable>
            </template>

        </Card>
    </div>
    <Dialog v-model:visible="show_driver" @close="driver={}" modal header="Изменить водителя"
            :style="{ 'max-width': '500px', width: '100%'}">
        <Driver v-if="driver.id" :driver="driver"/>
    </Dialog>
</template>

<style>
.carsHeader {
    background-color: var(--surface-ground) !important;
    color: var(--surface-50) !important;
}

.carsHeader:first-child {
    border-radius: 5px 0 0 5px;
}

.carsHeader:last-child {
    border-radius: 0 5px 5px 0;
}
</style>


