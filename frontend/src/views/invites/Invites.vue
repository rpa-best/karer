<script>
import {isManager} from "@/permissions";

export default {
    name: 'Invites',
    data() {
        return {
            statuses: {
                'created': {color: 'info', label: 'Принято'},
                'process': {color: 'warn', label: 'В обработке'},
                'done': {color: 'success', label: 'Успешно'},
                'canceled': {color: 'danger', label: 'Отклонено'},
            },
            types: {
                prepayment: {label: 'Предоплата'},
                deferment_payment: {label: 'Отсрочка платежа'},
                limit: {label: 'Лимит'},
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
                        type: 'deferment_payment',
                    },
                    {
                        id: 3,
                        date: '11.12.2024',
                        status: 'done',
                        type: 'limit',
                    },
                    {
                        id: 4,
                        date: '11.12.2024',
                        status: 'canceled',
                        type: 'prepayment',
                    }
                ]
            },
            statusOptions: [
                {
                    label: 'Все заявки',
                    value: 'all',
                },
                {
                    label: 'Открытые заявки',
                    value: 'created,process',
                },
                {
                    label: 'История отгрузок',
                    value: 'done,canceled',
                }
            ],
            filters: {
                status: 'all',
                org: null,
                limit: 10,
                offset: 0,
                search: null,
            },

        }
    },
    async mounted() {
        await this.fetch_data()
    },
    methods: {
        isManager,
        async onPage(e) {
            this.filters.offset = e.first
            await this.fetch_data()
        },
        async onFilter() {
            await this.fetch_data()
        },
        async fetch_data() {
            this.loading = true
            console.log(this.filters)
            setTimeout(() => {this.loading = false}, 3000)
        }
    },
}
</script>

<template>
    <div>
        <div class="flex justify-content-between align-items-center flex-wrap">
            <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Заявки</h2>
            <div class="flex md:flex-nowrap flex-wrap">
                <div class="md:mr-3 mb-3 w-full">
                    <IconField class="w-full">
                        <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full"/>
                        <InputIcon>
                            <i class="pi pi-search cursor-pointer" @click="onFilter"/>
                        </InputIcon>
                    </IconField>
                </div>
                <Select @value-change="onFilter" show-clear v-model="filters.org" :options="orgs" optionLabel="name" option-value="id" filter placeholder="Выберите организацию" class="w-full md:mr-3 mb-3" />
                <Button v-if="isManager()" label="Создать заявку" style="width: 300px" icon="pi pi-plus" class="mb-3 w-full" />
            </div>
        </div>

        <SelectButton @click="onFilter" class="mb-3" v-model="filters.status" :options="statusOptions" optionLabel="label" option-value="value" dataKey="label"/>

        <Card>
            <template #content>
                <DataTable size="large" :value="invites.results" paginator :rows="filters.limit" lazy
                           @page="onPage($event)" rowHover
                           :total-records="invites.count" :loading="loading" responsive-layout="scroll">
                    <Column field="id" header="Номер заявки" style="font-weight: 600; text-wrap: nowrap; text-align: center"
                            header-class="carsHeader"></Column>
                    <Column field="date" header="Дата создания" style="font-weight: 600; text-wrap: nowrap; text-align: center"
                            header-class="carsHeader"></Column>
                    <Column field="date" header="Тип" style="font-weight: 600; text-wrap: nowrap; text-align: center"
                            header-class="carsHeader">
                        <template #body="slotProps">
                            {{ types[slotProps.data.type].label }}
                        </template>
                    </Column>
                    <Column header="Статус" field="status" header-class="carsHeader" style="font-weight: 600; text-align: center">
                        <template #body="slotProps">
                            <Tag :value="statuses[slotProps.data.status].label"
                                 :severity="statuses[slotProps.data.status].color" class="text-nowrap"/>
                        </template>
                    </Column>
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

.p-togglebutton:before {
    background-color: var(--surface-card)!important;

}

.p-togglebutton-checked:before {
    background-color: var(--primary-color)!important;
}

.p-togglebutton-checked .p-togglebutton-label {
    color: var(--primary-contrast-color)!important;
}
</style>


