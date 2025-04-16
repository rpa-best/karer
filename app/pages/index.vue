<script>
import { isManager } from '@/permissions';
import { Plus } from "lucide-vue-next"
export default {
    name: 'Invites',
    components: { Plus },
    data() {
        return {
            statuses: {
                created: { color: 'info', label: 'Принято' },
                process: { color: 'warn', label: 'В обработке' },
                done: { color: 'success', label: 'Успешно' },
                canceled: { color: 'danger', label: 'Отклонено' }
            },
            types: {
                prepayment: { label: 'Предоплата' },
                deferment_payment: { label: 'Отсрочка платежа' },
                limit: { label: 'Лимит' }
            },
            loading: true,
            orgs: [],
            invites: {
                count: 20,
                results: []
            },
            statusOptions: [
                {
                    label: 'Все заявки',
                    value: 'all'
                },
                {
                    label: 'Открытые заявки',
                    value: 'created,process'
                },
                {
                    label: 'История отгрузок',
                    value: 'done,canceled'
                }
            ],
            filters: {
                status: 'all',
                org: null,
                limit: 10,
                offset: 0,
                search: null
            },
            show_invoice: false,
            invoice: {},
        };
    },
    async mounted() {
        await this.fetch_data();
        const {data} = await this.$api.get('/onec/organization/')
        this.orgs = data
    },
    methods: {
        isManager,
        rowClick(e) {
            this.show_invoice = true
            this.invoice = e.data
        },
        async onPage(e) {
            this.filters.offset = e.first;
            await this.fetch_data();
        },
        async onFilter() {
            await this.fetch_data();
        },
        async fetch_data() {
            this.loading = true;
            const { data } = await this.$api.get('/invoice/', {params: this.filters})
            this.invites = data
            this.loading = false;
        }
    }
};
</script>

<template>
    <loading :loading="loading">
        <div class="flex justify-between align-items-center flex-wrap">
            <h2 class="mb-3 text-3xl font-bold">Заявки</h2>
            <div class="flex md:flex-nowrap flex-wrap">
                <div class="md:mr-3 mb-3 w-full">
                    <IconField class="w-full">
                        <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full" />
                        <InputIcon>
                            <i class="pi pi-search cursor-pointer" @click="onFilter" />
                        </InputIcon>
                    </IconField>
                </div>
                <Select @value-change="onFilter" show-clear v-model="filters.org" :options="orgs" optionLabel="name"
                    option-value="uuid" filter placeholder="Выберите организацию" class="w-full md:mr-3 mb-3" />
                <Button v-if="isManager()" class="mb-3 w-full" @click="() => rowClick({data: {}})">
                    <Plus />
                    Создать заявку
                </Button>
            </div>
        </div>

        <SelectButton @click="onFilter" class="mb-3" v-model="filters.status" :options="statusOptions" optionLabel="label"
            option-value="value" dataKey="label" />

        <DataTable size="large" :value="invites.results" paginator :rows="filters.limit" lazy @page="onPage($event)"
            rowHover :total-records="invites.count" :loading="loading" responsive-layout="scroll" @row-click="rowClick">
            <Column field="number" header="Номер заявки"></Column>
            <Column field="created_at" header="Дата создания"></Column>
            <Column field="type" header="Тип">
                <template #body="slotProps">
                    {{ types[slotProps.data.type].label }}
                </template>
            </Column>
            <Column header="Статус" field="status">
                <template #body="slotProps">
                    <Tag :value="statuses[slotProps.data.status].label" :severity="statuses[slotProps.data.status].color"
                        class="text-nowrap" />
                </template>
            </Column>
            <template #empty> <p class="text-center"> Инвойси не найдены. </p></template>
        </DataTable>
    </loading>
    <Dialog v-model:visible="show_invoice" @close="invoice={}" modal header="Изменить инвойс"
            :style="{ 'max-width': '700px', width: '100%'}">
        <Invoice v-if="show_invoice" :invoice="invoice" @close="flag => {invoice = {}; show_invoice=false; flag ? fetch_data() : null}"/>
    </Dialog>
</template>
