<script setup lang="ts">
import {Form} from '@primevue/forms'
import {X} from 'lucide-vue-next'
import {isManager} from "~/permissions"
import { zodResolver } from '@primevue/forms/resolvers/zod'
import z from 'zod'
import { ref, computed } from 'vue'
import { useOrganization, useSpecification, useNomenclature } from '@/store/onec'
import type { Invoice } from '~/types/invoices'
import type { InvoiceNomenclature } from '~/types/invoices'
import type { Specification, Nomenclature } from '~/types/onec'
import { useInvoice } from '~/store/invoices'


const props = defineProps<{
  invoice: Invoice | undefined
}>()

const emit = defineEmits<{
  close: [flag?: boolean]
}>()

const organization = useOrganization()
const specification = useSpecification()
const nomenclature = useNomenclature()
const invoices = useInvoice()

const disabled = ref(false)
const invoiceNomenclatures = ref(props.invoice?.nomenclatures || [])
const editingRows = ref<InvoiceNomenclature[]>([])

const resolver = zodResolver(
  z.object({
    org: z.string(),
    specification: z.string(), 
    address: z.string(),
    comment: z.string().optional(),
  })
)

const nDisabled = computed(() => {
  return !['created', undefined, null].includes(props.invoice?.status) || !isManager()
})

async function mounted() {
  disabled.value = true
  await organization.fetchOrganizations()
  await specification.fetchSpecifications()
  await nomenclature.fetchNomenclatures()
  disabled.value = false
}

function removeRow(index: number) {
  invoiceNomenclatures.value.splice(index, 1)
}

function addRow() {
  const newN = {
    created_at: new Date().toISOString(),
    invoice: props.invoice?.id,
    nomenclature: null,
    value: 0
  }
  invoiceNomenclatures.value.push(newN)
  editingRows.value.push(newN)
}

async function save({values}: {values: any}) {
  disabled.value = true
  values.nomenclatures = invoiceNomenclatures.value
  try {
    if (props.invoice?.id) {
      await invoices.updateInvoice(props.invoice.id, values)
    } else {
      await invoices.createInvoice(values)
    }
    emit('close', true)
  } catch (e) {
    console.log(e)
  } finally {
    disabled.value = false
  }
}

mounted()
</script>

<template>
  <loading :loading="disabled">
    <Form v-slot="$form" :resolver="resolver" :initial-values="invoice" @submit="save" autocomplete="off">
      <div class="grid gap-8 grid-cols-3 mt-5">
        <div class="col-span-3">
          <FloatLabel>
            <Select emptyMessage="Пусто" required id="org" class="w-full" name="org" :disabled="nDisabled"
                    :options="organization.organizations" option-value="uuid" option-label="name"/>
            <label for="org" class="text-sm">Грузополучатель</label>
          </FloatLabel>
        </div>
        <div class="col-span-3">
          <FloatLabel>
            <Select @update:model-value="(value: string) => {
                      $form.address.value = specification.specifications?.find((s: Specification) => s.uuid === value)?.delivery_address
                    }" emptyMessage="Пусто" required id="specification" class="w-full" name="specification"
                    :disabled="nDisabled" :options="specification.specifications" option-value="uuid" option-label="name"/>
            <label for="specification" class="text-sm">Спецификация</label>
          </FloatLabel>
        </div>
        <div class="col-span-3">
          <FloatLabel>
            <InputText required id="address" class="w-full" name="address" :disabled="!!$form.address?.value"/>
            <label for="address" class="text-sm">Адрес поставки</label>
          </FloatLabel>
        </div>

        <div class="col-span-3">
          <FloatLabel>
            <Textarea id="comment" size="large" class="w-full" name="comment" :disabled="nDisabled"/>
            <label for="comment" class="text-sm">Комментарии</label>
          </FloatLabel>
        </div>

        <div class="col-span-3">
          <DataTable :key="invoiceNomenclatures.length" v-model:editingRows="invoiceNomenclatures"
                     :value="invoiceNomenclatures" editMode="row" dataKey="created_at">
            <Column field="nomenclature" header="Номенклатура">
              <template #editor="{ data, field }">
                <Select class="max-w-[250px]" :disabled="nDisabled" empty-message="Пусто"
                        placeholder="Выберите номенклатуру" v-model="data[field]" :options="nomenclature.nomenclatures"
                        option-value="uuid" option-label="name"/>
              </template>
            </Column>
            <Column field="value" header="Потребность">
              <template #editor="{ data, field }">
                <InputNumber :input-props="{autocomplete: 'off'}"
                             :suffix="` ${nomenclature.nomenclatures?.find((v: Nomenclature) => v.uuid === data?.nomenclature)?.unit}`"
                             :disabled="nDisabled" placeholder="Введите потребность" v-model="data[field]"/>
              </template>
            </Column>
            <Column v-if="!nDisabled" bodyStyle="text-align:center">
              <template #body="{index}">
                <div class="flex gap-3">
                  <X v-if="isManager()" class="cursor-pointer" @click="removeRow(index)"/>
                </div>
              </template>
            </Column>
            <template #footer>
              <Button v-if="!nDisabled && isManager()" @click="addRow" severity="info" class="w-full">Добавить
                номенклатуру
              </Button>
            </template>
          </DataTable>
        </div>
      </div>
      <slot name="buttons" :disabled="disabled">
        <div class="flex flex-row gap-3 mt-2">
          <Button @click="$emit('close')" class="w-full" severity="secondary">Отменить</Button>
          <Button v-if="isManager()" :disabled="nDisabled" :loading="disabled" type="submit" class="w-full">Сохранить
          </Button>
        </div>
      </slot>
      
    </Form>
  </loading>
</template>
