<script>
import Car from "./Car.vue"

export default {
    name: 'Cars',
    components: {Car},
    data() {
        return {
            loading: true,
            car: {},
            show_car: false,
            cars: [
                {
                    id: 1,
                    number: 'K777KKK',
                    mark: 'KAMAZ',
                    model: '43118',
                    vin: '435342543n2jn4i2',
                }
            ],
            filters: {
                search: null
            }
        }
    },
    async mounted() {
        await this.fetch_data()
    },
    methods: {
        rowClick(e) {
            this.show_car = true
            this.car = e.data
        },
        async onFilter() {
            await this.fetch_data()
        },
        async fetch_data() {
            this.loading = true
            console.log(this.filters)
            setTimeout(() => {this.loading = false}, 3000)
        }
    }
}
</script>

<template>
    <div>
        <div class="flex justify-content-between align-items-center flex-wrap">
            <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Автомобили</h2>
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
                <DataTable size="large" :value="cars" lazy :loading="loading" @row-click="rowClick" rowHover>
                    <Column field="number" header="Номер" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="mark" header="Марка" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="model" header="Модель" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="vin" header="VIN-Номер" style="font-weight: 600" header-class="carsHeader"></Column>
                </DataTable>
            </template>
        </Card>
    </div>
    <Dialog v-model:visible="show_car" @close="car={}" modal header="Изменить автомобиль" :style="{ 'max-width': '500px', width: '100%'}">
        <Car v-if="car.id" :car="car" />
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

