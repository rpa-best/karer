<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {Pen, Plus} from "lucide-vue-next"
import type { DataTablePageEvent } from 'primevue/datatable';
import type { InvoiceParams } from '~/store/invoices';
import { useInvoice } from '~/store/invoices';
import { useOrganization } from '~/store/onec';
import { isManager, isLogist } from '~/permissions';
import type { Invoice } from '~/types/invoices';

const statuses: {[key: string]: {color: string, label: string}} = {
    created: { color: 'info', label: 'Принято' },
    process: { color: 'warn', label: 'В обработке' },
    done: { color: 'success', label: 'Успешно' },
    canceled: { color: 'danger', label: 'Отклонено' }
}

const types: {[key: string]: {label: string}} = {
    prepayment: { label: 'Предоплата' },
    deferment_payment: { label: 'Отсрочка платежа' },
    limit: { label: 'Лимит' }
}

const statusOptions: {label: string, value: string}[] = [
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
]

const filters: Ref<InvoiceParams> = ref({
    status: 'all',
    org: null,
    limit: 10,
    offset: 0,
    search: null,
    type: null,
    specification: null,
    ordering: null
})

const loading = ref(true)
const show_invoice = ref(false)
const invoice: Ref<Invoice | undefined> = ref(undefined)
const expandedRowGroups = ref(null)
const organizations = useOrganization()
const invites = useInvoice()

const rowClick = (data: Invoice | undefined = undefined) => {
    show_invoice.value = true
    invoice.value = data
}

const onPage = async (e: DataTablePageEvent) => {
    filters.value.offset = e.first
    await fetch_data()
}

onMounted(async () => {
    await fetch_data()
    await organizations.fetchOrganizations()
})

async function onFilter() {
    await fetch_data();
}

async function fetch_data() {
    loading.value = true;
    await invites.fetchInvoices(filters.value)
    loading.value = false;
}
</script>

<template>
    <Loading :loading="loading">
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
                <Select @value-change="onFilter" show-clear v-model="filters.org" :options="organizations.organizations" optionLabel="name"
                    option-value="uuid" filter placeholder="Выберите организацию" class="w-full md:mr-3 mb-3" />
                <Button v-if="isManager()" class="mb-3 w-full" @click="() => rowClick()">
                    <Plus />
                    Создать заявку
                </Button>
            </div>
        </div>

        <SelectButton @click="onFilter" class="mb-3" v-model="filters.status" :options="statusOptions" optionLabel="label"
            option-value="value" dataKey="label" />

        <DataTable size="large" :value="invites.invoices?.results" paginator :rows="filters.limit" lazy @page="onPage"
            rowHover :total-records="invites.invoices?.count" :loading="loading" responsive-layout="scroll"
                   v-model:expandedRows="expandedRowGroups" dataKey="id">
            <Column expander v-if="isLogist()"></Column>
            <Column field="number" header="Номер заявки"></Column>
            <Column field="created_at" header="Дата создания"></Column>
            <Column field="type" header="Условия отгрузки">
                <template #body="slotProps">
                    {{ slotProps.data?.type ? types[slotProps.data.type]?.label : '' }}
                </template>
            </Column>
            <Column header="Статус" field="status">
                <template #body="slotProps">
                    <Tag v-if="slotProps.data?.status" :value="statuses[slotProps.data.status]?.label" :severity="statuses[slotProps.data.status]?.color"
                        class="text-nowrap" />
                </template>
            </Column>
          <Column>
            <template #body="{data}">
              <Button @click="rowClick(data)" severity="help" rounded class="size-8 !p-2">
                <Pen />
              </Button>
            </template>
          </Column>
            <template #empty> <p class="text-center"> Заявки не найдены. </p></template>
          <template #expansion="{data}">
            <div class="w-full">
              <Orders :invoice="data" />
            </div>
          </template>
        </DataTable>
    </Loading>
    <Dialog v-model:visible="show_invoice" @close="invoice=undefined" modal :header="invoice?.id ? 'Изменить заявку' : 'Создать заявку'"
            :style="{ 'max-width': '700px', width: '100%'}">
        <Invoice v-if="show_invoice" :invoice="invoice" @close="(flag: boolean | undefined) => {invoice = undefined; show_invoice=false; flag ? fetch_data() : null}"/>
    </Dialog>
</template>
