<script>
import { Plus } from "lucide-vue-next"

export default {
    name: 'Cars',
    components: {Plus},
    data() {
        return {
            loading: true,
            car: {},
            show_car: false,
            cars: [],
            filters: {
                search: null
            }
        };
    },
    async mounted() {
        await this.fetch_data();
    },
    methods: {
        rowClick(e) {
            this.show_car = true;
            this.car = e.data;
        },
        async onFilter() {
            await this.fetch_data();
        },
        async fetch_data() {
            this.loading = true;
            const { data } = await this.$api.get('/car/', {params: this.filters})
            this.cars = data
            this.loading = false;
        }
    }
};
</script>

<template>
    <loading :loading="loading">
        <div class="flex justify-between align-items-center flex-wrap">
            <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Автомобили</h2>
            <div class="flex md:flex-nowrap gap-3 flex-wrap md:w-auto w-full">
                <IconField class="w-full mb-3">
                    <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full" />
                    <InputIcon>
                        <i class="pi pi-search cursor-pointer" @click="onFilter" />
                    </InputIcon>
                </IconField>
                <Button class="mb-3 w-full" @click="() => rowClick({data: {}})">
                    <Plus />
                    Добавить автомобиль
                </Button>
            </div>
        </div>
        <Card>
            <template #content>
                <DataTable size="large" :value="cars" lazy :loading="loading" @row-click="rowClick" rowHover>
                    <Column field="number" header="Номер" style="font-weight: 600"></Column>
                    <Column field="marka" header="Марка" style="font-weight: 600"></Column>
                    <Column field="model" header="Модель" style="font-weight: 600"></Column>
                    <Column field="vin" header="VIN-Номер" style="font-weight: 600"></Column>
                    <template #empty> <p class="text-center"> Машины не найдены. </p></template>
                </DataTable>
            </template>
        </Card>
    </loading>
    <Dialog v-model:visible="show_car" @close="car = {}" modal header="Изменить автомобиль" :style="{ 'max-width': '500px', width: '100%' }">
        <Car v-if="show_car" :car="car" @close="flag => {car = {}; show_car=false; flag ? fetch_data() : null}" />
    </Dialog>
</template>

