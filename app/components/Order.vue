<script>
import { Form } from '@primevue/forms';

export default {
    name: 'Order',
    props: ['order', 'invoice'],
    emits: ['close'],
    components: { Form, },
    data() {
        const myOrder = JSON.parse(JSON.stringify(this.order))
        myOrder.car = myOrder.car ? myOrder.car.id : null
        myOrder.driver = myOrder.driver ? myOrder.driver.id : null
        myOrder.nomenclature = myOrder.nomenclature ? myOrder.nomenclature.uuid : null
        return {
            myOrder,
            cars: [],
            drivers: [],
            nomenclatures: [],
            disabled: false,
        };
    },
    async mounted() {
        this.disabled = true
        let r = null
        r = await this.$api.get('/car/')
        this.cars = r.data

        r = await this.$api.get('/driver/')
        this.drivers = r.data

        r = await this.$api.get(`/invoice/${this.invoice.id}/available_nomenclature/`)
        this.nomenclatures = r.data
        this.disabled = false
    },
    methods: {
        async save({ values }) {
            this.disabled = true
            try {
                if (this.order.uuid) {
                    await this.$api.patch(`/invoice/${this.invoice.id}/order/${this.order.uuid}/`, values)
                } else {
                    await this.$api.post(`/invoice/${this.invoice.id}/order/`, values)
                }
                this.$emit('close', true)
            } catch (e) { console.log(e); } finally {
                this.disabled = false
            }
        }
    }
};
</script>

<template>
  <loading :loading="disabled">
    <Form :initial-values="myOrder" @submit="save">
        <div class="grid gap-8 grid-cols-6 mt-5">
            <div class="col-span-6">
                <FloatLabel>
                    <Select emptyMessage="Пусто" required id="car" style="width: 100%" name="car" :disabled="order.done" :options="cars" option-value="id" option-label="number" />
                    <label for="car" style="font-size: 12px">Машина</label>
                </FloatLabel>
            </div>
            <div class="col-span-6">
                <FloatLabel>
                    <Select emptyMessage="Пусто" required id="driver" style="width: 100%" name="driver" :disabled="order.done" :options="drivers" option-value="id" option-label="name" />
                    <label for="driver" style="font-size: 12px">Водитель</label>
                </FloatLabel>
            </div>
            <div class="col-span-6">
                <FloatLabel>
                    <InputText required id="address" style="width: 100%" name="address" :disabled="order.done" />
                    <label for="address" style="font-size: 12px">Адрес поставки</label>
                </FloatLabel>
            </div>
            <div class="col-span-6">
                <FloatLabel>
                    <Select emptyMessage="Пусто" required id="nomenclature" style="width: 100%" name="nomenclature" :disabled="order.done" :options="nomenclatures" option-value="uuid" option-label="name" />
                    <label for="nomenclature" style="font-size: 12px">Номенклатура</label>
                </FloatLabel>
            </div>
            <div class="col-span-3">
                <FloatLabel>
                    <InputNumber required id="per_price" style="width: 100%" name="per_price" :disabled="order.done" />
                    <label for="per_price" style="font-size: 12px">Стоимость за ед.</label>
                </FloatLabel>
            </div>
            <div class="col-span-3">
                <FloatLabel>
                    <InputNumber required id="price" style="width: 100%" name="price" :disabled="order.done" />
                    <label for="price" style="font-size: 12px">Сумма</label>
                </FloatLabel>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputNumber id="additive" style="width: 100%" name="additive" :disabled="order.done" />
                    <label for="additive" style="font-size: 12px">Добавка</label>
                </FloatLabel>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputNumber id="order" style="width: 100%" name="order" :disabled="order.done" />
                    <label for="order" style="font-size: 12px">Заказ</label>
                </FloatLabel>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputNumber id="fact" style="width: 100%" name="fact" :disabled="order.done" />
                    <label for="fact" style="font-size: 12px">Факт</label>
                </FloatLabel>
            </div>
        </div>
        <div class="flex flex-row gap-3 mt-2">
            <Button @click="$emit('close')" class="w-full" severity="secondary">Отменить</Button>
            <Button v-if="!order.done" :disabled="disabled" :loading="disabled" type="submit" class="w-full">Сохранить</Button>
        </div>
    </Form>
  </loading>
</template>
