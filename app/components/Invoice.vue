<script>
import { Form } from '@primevue/forms';
import { Check, X } from 'lucide-vue-next';
import {isLogist, isManager} from "~/permissions.js";
export default {
    name: 'Invoice',
    props: ['invoice'],
    emits: ['close'],
    components: { Form, Check, X },
    data() {
        return {
            orgs: [],
            specifications: [],
            nomenclatures: [],
            disabled: false,
            invoiceNomenclatures: this.invoice.nomenclatures || [],
            editingRows: [],
            show_orders: false,
        };
    },
    computed: {
        nDisabled() {
            return !['created', undefined, null].includes(this.invoice.status) || !this.isManager()
        }
    },
    async mounted() {
        this.disabled = true
        let r = null
        r = await this.$api.get('/onec/organization/')
        this.orgs = r.data

        r = await this.$api.get('/onec/specification/')
        this.specifications = r.data

        r = await this.$api.get('/onec/nomenclature/')
        this.nomenclatures = r.data
        this.disabled = false
    },
    methods: {
      isManager,
      isLogist,
        removeRow (index) {
            this.invoiceNomenclatures.splice(index, 1)
        },
        addRow() {
            const newN = {created_at: new Date(), invoice: this.invoice.id}
            this.invoiceNomenclatures.push(newN)
            this.editingRows.push(newN)
        },
        async save({ values }) {
            this.disabled = true
            values.nomenclatures = this.invoiceNomenclatures
            try {
                if (this.invoice.id) {
                    await this.$api.patch(`/invoice/${this.invoice.id}/`, values)
                } else {
                    await this.$api.post('/invoice/', values)
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
    <Form :initial-values="invoice" @submit="save">
        <div class="grid gap-8 grid-cols-3 mt-5">
            <div class="col-span-3">
                <FloatLabel>
                    <Select emptyMessage="Пусто" required id="org" style="width: 100%" name="org" :disabled="nDisabled" :options="orgs" option-value="uuid" option-label="name" />
                    <label for="org" style="font-size: 12px">Грузаполучатель</label>
                </FloatLabel>
            </div>
            <div class="col-span-3">
                <FloatLabel>
                    <Select emptyMessage="Пусто" required id="specification" style="width: 100%" name="specification" :disabled="nDisabled" :options="specifications" option-value="uuid" option-label="name" />
                    <label for="specification" style="font-size: 12px">Спецификация</label>
                </FloatLabel>
            </div>
            <div class="col-span-3">
                <FloatLabel>
                    <InputText required id="address" style="width: 100%" name="address" :disabled="nDisabled" />
                    <label for="address" style="font-size: 12px">Адрес поставки</label>
                </FloatLabel>
            </div>

            <div class="col-span-3">
                <DataTable :key="invoiceNomenclatures.length" v-model:editingRows="invoiceNomenclatures" :value="invoiceNomenclatures" editMode="row" dataKey="created_at">
                    <Column field="nomenclature" header="Номенклатура">
                        <template #editor="{ data, field }">
                            <Select class="max-w-[250px]" :disabled="nDisabled" empty-message="Пусто" placeholder="Выберите номенклатуру" v-model="data[field]" :options="nomenclatures" option-value="uuid" option-label="name"/>
                        </template>
                    </Column>
                    <Column field="value" header="Потребность">
                        <template #editor="{ data, field }">
                            <InputNumber suffix=" кг" :disabled="nDisabled" placeholder="Введите потребность" v-model="data[field]" />
                        </template>
                    </Column>
                    <Column v-if="!nDisabled" bodyStyle="text-align:center">
                        <template #body="{index}">
                            <div class="flex gap-3">
                                <X v-if="isManager()" class="cursor-pointer" @click="removeRow(index)" />
                            </div>
                        </template>
                    </Column>
                    <template #footer>
                        <Button v-if="!nDisabled && isManager()" @click="addRow" severity="info" class="w-full">Добавить номенклатура</Button>
                    </template>
                </DataTable>
            </div>
        </div>
        <div class="flex flex-row gap-3 mt-2">
            <Button @click="$emit('close')" class="w-full" severity="secondary">Отменить</Button>
            <Button @click="show_orders = true" class="w-full" severity="help" :disabled="!['created', 'process'].includes(invoice.status)" v-if="invoice.id && isLogist()">Заказы</Button>
            <Button v-if="isManager()" :disabled="nDisabled" :loading="disabled" type="submit" class="w-full">Сохранить</Button>
        </div>
    </Form>
  </loading>
    <Dialog v-model:visible="show_orders" modal header="Заказы"
            :style="{ 'max-width': '90vw', width: '100%'}">
        <Orders v-if="show_orders" :invoice="invoice" @close="show_orders=false"/>
    </Dialog>
</template>
