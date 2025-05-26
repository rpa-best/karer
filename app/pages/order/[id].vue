<template>
    <div class="grid 2xl:grid-cols-2 gap-4">
        <div class="col-span-1 bg-white rounded-lg p-4">
            <h1 v-if="invoice" class="text-2xl font-bold pb-3">Заявка №: <span class="text-primary">{{ invoice.number }}</span></h1>
            <Invoice v-if="invoice" :invoice="invoice">
                <template #buttons>
                    <Button @click="router.push('/')" class="w-full" severity="secondary">Назад</Button> 
                </template>
            </Invoice>
        </div>
        <div class="col-span-1 bg-white rounded-lg p-4">
            <h1 v-if="order" class="text-2xl font-bold pb-3">Заказ №: <span class="text-primary">{{ order.uuid }}</span></h1>

            <Order v-if="order && invoice" :order="order" :invoice="invoice">
                <template #buttons="{disabled}">
                    <div class="flex md:flex-row flex-col gap-3 mt-2">
                        <Button v-if="!order.done" @click="deleteOrder" class="w-full" severity="danger">Удалить</Button>
                        <Button v-if="!order.done" @click="sendCareer" class="w-full" severity="warn">Отправить в карерь</Button>
                        <Button v-if="!order.done" :disabled="disabled" :loading="disabled" type="submit" class="w-full">Сохранить</Button>
                    </div>
                </template>
            </Order>
        </div>
        <div class="col-span-1 bg-white rounded-lg p-4">
            <h1 v-if="order" class="text-2xl font-bold pb-3">Комментарий водителя</h1>
            <DriverComment v-if="order && invoice" :order="order" :invoice="invoice"/>
        </div>
    </div>
</template>

<script setup lang="ts">
import { isLogist } from '~/permissions'
import { OrderService } from '~/services'
import { InvoiceService } from '~/services/invoice'
import type { Order, Invoice } from '~/types/invoices'
import { useQuery } from '@tanstack/vue-query'

const route = useRoute()
const router = useRouter()
const orderService = new OrderService()
const invoiceService = new InvoiceService()

if (!isLogist()) {
    router.push('/')
}

const {data: order} = useQuery({
    queryKey: computed(() => ['order', route.params.id]),
    queryFn: async () => await orderService.get<Order>(route.params.id as string)
})

const {data: invoice} = useQuery({
    queryKey: computed(() => ['invoice', order.value?.invoice]),
    queryFn: async () => await invoiceService.get<Invoice>(order.value?.invoice as number),
    enabled: computed(() => !!order.value?.invoice)
})

const sendCareer = async () => {
    if (order.value && invoice.value) {
        await invoiceService.order.sendCareer(invoice.value.id, order.value.uuid)
    }
}

const deleteOrder = async () => {
    if (order.value && invoice.value) {
        await invoiceService.order.delete(order.value.uuid, {}, {invoice_id: invoice.value.id})
        await router.push('/')
    }
}
</script>