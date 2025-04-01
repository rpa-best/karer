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
            orgs: [
                {
                    id: 1,
                    name: 'ООО “Примера”'
                }
            ],
            invites: {
                count: 20,
                results: [
                    {
                        id: 1,
                        date: '11.12.2024',
                        status: 'created',
                        type: 'prepayment'
                    },
                    {
                        id: 2,
                        date: '11.12.2024',
                        status: 'process',
                        type: 'deferment_payment'
                    },
                    {
                        id: 3,
                        date: '11.12.2024',
                        status: 'done',
                        type: 'limit'
                    },
                    {
                        id: 4,
                        date: '11.12.2024',
                        status: 'canceled',
                        type: 'prepayment'
                    }
                ]
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
            }
        };
    },
    async mounted() {
        await this.fetch_data();
    },
    methods: {
        isManager,
        async onPage(e) {
            this.filters.offset = e.first;
            await this.fetch_data();
        },
        async onFilter() {
            await this.fetch_data();
        },
        async fetch_data() {
            this.loading = true;
            console.log(this.filters);
            setTimeout(() => {
                this.loading = false;
            }, 3000);
        }
    }
};
</script>

<template>
    <div>
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
                    option-value="id" filter placeholder="Выберите организацию" class="w-full md:mr-3 mb-3" />
                <Button v-if="isManager()" class="mb-3 w-full">
                    <Plus />
                    Создать заявку
                </Button>
            </div>
        </div>

        <SelectButton @click="onFilter" class="mb-3" v-model="filters.status" :options="statusOptions" optionLabel="label"
            option-value="value" dataKey="label" />

        <DataTable size="large" :value="invites.results" paginator :rows="filters.limit" lazy @page="onPage($event)"
            rowHover :total-records="invites.count" :loading="loading" responsive-layout="scroll">
            <Column field="id" header="Номер заявки" style="font-weight: 600; text-wrap: nowrap; text-align: center"
               ></Column>
            <Column field="date" header="Дата создания" style="font-weight: 600; text-wrap: nowrap; text-align: center"
               ></Column>
            <Column field="date" header="Тип" style="font-weight: 600; text-wrap: nowrap; text-align: center"
               >
                <template #body="slotProps">
                    {{ types[slotProps.data.type].label }}
                </template>
            </Column>
            <Column header="Статус" field="status" style="font-weight: 600; text-align: center">
                <template #body="slotProps">
                    <Tag :value="statuses[slotProps.data.status].label" :severity="statuses[slotProps.data.status].color"
                        class="text-nowrap" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>
