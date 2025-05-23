<script setup lang="ts">
import { useToast } from 'primevue/usetoast'
import z from 'zod'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import type { Order, Invoice, OrderForm } from '~/types/invoices'
import type { Car } from '~/types/car'
import type { Driver } from '~/types/driver'
import type { Nomenclature } from '~/types/onec'
import type { FormSubmitEvent } from '@primevue/forms'
import { CarService, DriverService, NomenclatureService } from '~/services'
import { InvoiceService } from '~/services/invoice'

const { order, invoice } = defineProps<{
  order: Order | {}
  invoice: Invoice
}>()

const emit = defineEmits<{
  close: [success?: boolean]
}>()

const myOrder = ref<OrderForm>({
  ...JSON.parse(JSON.stringify(order)),
  address: invoice?.address ?? (order as Order).address,
  car: (order as Order).car ? (order as Order).car.id : null,
  driver: (order as Order).driver ? (order as Order).driver.id : null,
  nomenclature: (order as Order).nomenclature ? (order as Order).nomenclature.uuid : null
})

const carService = new CarService()
const driverService = new DriverService()
const nomenclatureService = new NomenclatureService()
const invoiceService = new InvoiceService()

const {data: cars} = carService.list<Car[]>()
const {data: drivers} = driverService.list<Driver[]>()
const {data: nomenclatures} = nomenclatureService.list<Nomenclature[]>()

const disabled = ref(true)
const toast = useToast()

const resolver = zodResolver(
  z.object({
    car: z.number(),
    driver: z.number(), 
    address: z.string(),
    nomenclature: z.string(),
    additive: z.number(),
    order: z.number(),
    price: z.number(),
    per_price: z.number(),
    comment: z.string().nullable(),
  })
)

onMounted(async () => {
  disabled.value = false
})

function select_nomenclature({value}: {value: any}, form: any) {
  const nomenclature = nomenclatures.value?.find((n: Nomenclature) => n.uuid === value)
  if (nomenclature) {
    if (!nomenclature.per_price) {
      toast.add({severity: 'warn', summary: 'Ошибка', detail: 'У номенклатуры не указана цена', life: 3000})
      form.per_price.value = null
      form.price.value = null 
      form.per_price.invalid = true
      form.price.invalid = true
      return
    }
    form.per_price.invalid = false
    form.price.invalid = false
    form.per_price.value = nomenclature.per_price
    form.price.value = nomenclature.per_price * (form.fact.value ? form.fact.value : form.order.value || 0)
  }
}

async function save({values, valid}: FormSubmitEvent) {
  if (!valid) return
  disabled.value = true
  try {
    if (myOrder.value.uuid) {
      await invoiceService.order.update(myOrder.value.uuid, values as OrderForm, {}, {invoice_id: invoice.id})
    } else {
      await invoiceService.order.create(values as OrderForm, {}, {invoice_id: invoice.id})
    }
    emit('close', true)
  } catch (e) {
    console.log(e)
    myOrder.value = values as OrderForm
  } finally {
    disabled.value = false
  }
}

function getUnit(nomenclature: string) {
  return nomenclatures.value?.find((n: Nomenclature) => n.uuid === nomenclature)?.unit
}
</script>

<template>
  <Loading :loading="disabled">
    <Form v-slot="$form" :initial-values="myOrder" :resolver="resolver" @submit="save" autocomplete="off">
      <div class="grid gap-8 grid-cols-6 mt-5">
        <div class="col-span-6">
          <FloatLabel>
            <Select emptyMessage="Пусто" required id="car" class="w-full" name="car" :disabled="myOrder.done"
                    :options="cars" option-value="id" option-label="number"/>
            <label for="car" style="font-size: 12px">Машина</label>
          </FloatLabel>
        </div>
        <div class="col-span-6">
          <FloatLabel>
            <Select emptyMessage="Пусто" required id="driver" style="width: 100%" name="driver" :disabled="myOrder.done"
                    :options="drivers" option-value="id" option-label="name"/>
            <label for="driver" style="font-size: 12px">Водитель</label>
          </FloatLabel>
        </div>
        <div class="col-span-6">
          <FloatLabel>
            <InputText required id="address" style="width: 100%" name="address" :disabled="!!$form.address?.value"/>
            <label for="address" style="font-size: 12px">Адрес поставки</label>
          </FloatLabel>
        </div>
        <div class="col-span-6">
          <FloatLabel>
            <Select @change="(e: any) => select_nomenclature(e, $form)" emptyMessage="Пусто" required id="nomenclature"
                    style="width: 100%" name="nomenclature" :disabled="myOrder.done" :options="nomenclatures"
                    option-value="uuid" option-label="name"/>
            <label for="nomenclature" style="font-size: 12px">Номенклатура</label>
          </FloatLabel>
        </div>

        <div class="lg:col-span-2 col-span-6">
          <FloatLabel>
            <InputNumber required 
                         :suffix="` ${getUnit($form.nomenclature?.value)}`"
                         id="additive" style="width: 100%" name="additive" :disabled="myOrder.done"/>
            <label for="additive" style="font-size: 12px">Добавка</label>
          </FloatLabel>
        </div>
        <div class="lg:col-span-2 col-span-6">
          <FloatLabel>
            <InputNumber required
                         @update:model-value="(value: number) => $form.price.value = $form.per_price?.value * ($form.fact?.value ? $form.fact.value : value)"
                         :suffix="` ${getUnit($form.nomenclature?.value)}`"
                         id="order" style="width: 100%" name="order" :disabled="myOrder.done"/>
            <label for="order" style="font-size: 12px">Количество на отгрузку</label>
          </FloatLabel>
        </div>
        <div class="lg:col-span-2 col-span-6">
          <FloatLabel>
            <InputNumber required 
                         :suffix="` ${getUnit($form.nomenclature?.value)}`"
                         id="fact" style="width: 100%" name="fact" :disabled="true"/>
            <label for="fact" style="font-size: 12px">Факт</label>
          </FloatLabel>
        </div>
        <div class="col-span-3">
          <FloatLabel>
            <InputNumber 
                suffix=" ₽"
                required id="per_price" style="width: 100%" name="per_price" :disabled="true"/>
            <label for="per_price" style="font-size: 12px">Стоимость за ед.</label>
          </FloatLabel>
        </div>
        <div class="col-span-3">
          <FloatLabel>
            <InputNumber 
                suffix=" ₽"
                required id="price" style="width: 100%" name="price" :disabled="true"/>
            <label for="price" style="font-size: 12px">Сумма</label>
          </FloatLabel>
        </div>
        <div class="col-span-6">
          <FloatLabel>
            <Textarea id="comment" size="large" class="w-full" name="comment"/>
            <label for="comment" class="text-sm">Комментарий</label>
          </FloatLabel>
        </div>
      </div>
      <slot name="buttons" :disabled="disabled">
        <div class="flex flex-row gap-3 mt-2">
            <Button @click="$emit('close')" class="w-full" severity="secondary">Отменить</Button>
            <Button v-if="!myOrder.done" :disabled="disabled" :loading="disabled" type="submit" class="w-full">Сохранить</Button>
        </div>
      </slot>
    </Form>
  </Loading>
</template>
