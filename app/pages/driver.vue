<script>
import { Plus } from "lucide-vue-next"

export default {
    name: 'Drivers',
    components: {Plus},
    data() {
        return {
            loading: true,
            driver: {},
            show_driver: false,
            drivers: [],
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
            const { data } = await this.$api.get('/driver/', {params: this.filters})
            this.drivers = data
            this.loading = false
        }
    }
}
</script>

<template>
    <div>
        <div class="flex justify-between align-items-center flex-wrap">
            <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Водители</h2>
            <div class="flex gap-3 md:flex-nowrap flex-wrap md:w-auto w-full">
                <IconField class="w-full">
                    <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full"/>
                    <InputIcon>
                        <i class="pi pi-search cursor-pointer" @click="onFilter"/>
                    </InputIcon>
                </IconField>
                <Button class="mb-3 w-full" @click="() => rowClick({data: {}})">
                    <Plus />
                    Добавить водителя
                </Button>
            </div>
        </div>
        <Card>
            <template #content>
                <DataTable size="large" :value="drivers" :loading="loading" lazy @row-click="rowClick" rowHover>
                    <Column field="id" header="ID" style="font-weight: 600"></Column>
                    <Column field="name" header="ФИО" style="font-weight: 600"></Column>
                    <Column field="phone" header="Телефон" style="font-weight: 600"></Column>
                    <template #empty> <p class="text-center"> Водители не найдены. </p></template>
                </DataTable>
            </template>

        </Card>
    </div>
    <Dialog v-model:visible="show_driver" @close="driver={}" modal header="Изменить водителя"
            :style="{ 'max-width': '500px', width: '100%'}">
        <Driver v-if="show_driver" :driver="driver" @close="flag => {driver = {}; show_driver=false; flag ? fetch_data() : null}"/>
    </Dialog>
</template>