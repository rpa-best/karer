<script>
import { Plus, Check, X, Pen } from "lucide-vue-next"
export default {
    name: 'Order',
    props: ['invoice'],
    components: {Plus, X, Check, Pen},
    data() {
        return {
            loading: true,
            orders: [],
            order: {},
            show_order: false,
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
            this.show_order = true
            this.order = e.data
        },
        async onFilter() {
            await this.fetch_data()
        },
        async fetch_data() {
            this.loading = true
            const { data } = await this.$api.get(`/invoice/${this.invoice.id}/order/`, {params: this.filters})
            this.orders = data
            this.loading = false
        },
        confirmDelete(event, data) {
            this.$confirm.require({
                target: event.currentTarget,
                message: 'Вы хотите удалить эту запись?',
                rejectProps: {
                    label: 'Назад',
                    severity: 'secondary',
                    outlined: true
                },
                acceptProps: {
                    label: 'Удалить',
                    severity: 'danger'
                },
                accept: async () => {
                    await this.$api.delete(`/invoice/${this.invoice.id}/order/${data.uuid}/`)
                    await this.fetch_data()
                },
            });
        }
    }
}
</script>

<template>
    <div>
        <div class="flex justify-between align-items-center flex-wrap">
            <IconField class="mb-3">
                <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full" />
                <InputIcon>
                    <i class="pi pi-search cursor-pointer" @click="onFilter" />
                </InputIcon>
            </IconField>
            <div class="flex md:flex-nowrap gap-3 flex-wrap md:w-auto w-full">
                <Button class="mb-3 w-full" @click="() => rowClick({data: {}})">
                    <Plus />
                    Добавить заказ
                </Button>
            </div>
        </div>
        <DataTable size="large" :value="orders" :loading="loading" lazy @row-click="rowClick" rowHover>
            <Column field="created_at" header="Дата" style="font-weight: 600"></Column>
            <Column field="car.number" header="Авто" style="font-weight: 600"></Column>
            <Column field="driver.name" header="Водитель" style="font-weight: 600"></Column>
            <Column field="address" header="Адрес поставки" style="font-weight: 600"></Column>
            <Column field="nomenclature.name" header="Номенклатура" style="font-weight: 600"></Column>
            <Column field="per_price" header="Стоимость за ед." style="font-weight: 600"></Column>
            <Column field="price" header="Сумма" style="font-weight: 600"></Column>
            <Column field="additive" header="Добавка" style="font-weight: 600"></Column>
            <Column field="order" header="Заказ" style="font-weight: 600"></Column>
            <Column field="fact" header="Факт" style="font-weight: 600"></Column>
            <Column class="flex justify-center">
                <template #body="{data}">
                    <Button v-if="data.done" severity="success" rounded class="size-8 p-1">
                        <Check/>
                    </Button>
                    <div v-else class="flex gap-2">
                        <Button @click="rowClick({data: data})" severity="help" rounded class="size-8 p-2">
                            <Pen />
                        </Button>
                        <Button @click="confirmDelete($event, data)" severity="danger" rounded class="size-8 p-2">
                            <X />
                        </Button>
                    </div>
                </template>
            </Column>
            <template #empty> <p class="text-center"> Заказы не найдены. </p></template>
        </DataTable>
    </div>
    <Dialog v-model:visible="show_order" modal header="Заказ"
            :style="{ 'max-width': '700px', width: '100%'}">
        <Order v-if="show_order" :order="order" :invoice="invoice" @close="flag => {order = {}; show_order=false; flag ? fetch_data() : null}"/>
    </Dialog>
    <ConfirmPopup></ConfirmPopup>
</template>