<script>
export default {
    name: 'Cars',
    data() {
        return {
            loading: true,
            cars: [
                {
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
        <div class="flex justify-content-between align-items-center mb-3">
            <h2 style="font-size: 24px; font-weight: bold">Автомобили</h2>
            <IconField>
                <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter"/>
                <InputIcon>
                    <i class="pi pi-search cursor-pointer" @click="onFilter"/>
                </InputIcon>
            </IconField>
        </div>
        <Card>
            <template #content>
                <DataTable size="large" :value="cars" lazy :loading="loading">
                    <Column field="number" header="Номер" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="mark" header="Марка" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="model" header="Модель" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="vin" header="VIN-Номер" style="font-weight: 600" header-class="carsHeader"></Column>
                </DataTable>
            </template>

        </Card>
    </div>

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

