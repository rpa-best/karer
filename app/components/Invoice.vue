<script setup lang="ts">
import {Form} from '@primevue/forms'
import {X} from 'lucide-vue-next'
import {isManager} from "~/permissions"
import { zodResolver } from '@primevue/forms/resolvers/zod'
import z from 'zod'
import { ref, computed } from 'vue'
import type { Invoice } from '~/types/invoices'
import type { InvoiceNomenclature } from '~/types/invoices'
import type { Specification, Nomenclature, Organization } from '~/types/onec'
import { InvoiceService } from '~/services/invoice'
import { OrganizationService, SpecificationService, NomenclatureService } from '~/services'
import { useToast } from 'primevue/usetoast'

const props = defineProps<{
  invoice: Invoice | undefined
}>()

const emit = defineEmits<{
  close: [flag?: boolean]
}>()
const toast = useToast()
const organizationService = new OrganizationService()
const specificationService = new SpecificationService()
const nomenclatureService = new NomenclatureService()
const invoiceService = new InvoiceService()

const {data: organizations} = organizationService.list<Organization[]>()
const {data: specifications} = specificationService.list<Specification[]>()
const {data: nomenclatures} = nomenclatureService.list<Nomenclature[]>()

const disabled = ref(true)
const invoiceNomenclatures = ref(props.invoice?.nomenclatures || [])
const editingRows = ref<InvoiceNomenclature[]>([])

const resolver = zodResolver(
  z.object({
    org: z.string(),
    specification: z.string(), 
    address: z.string(),
    comment: z.string().nullable(),
  })
)

const nDisabled = computed(() => {
  return !['created', undefined, null].includes(props.invoice?.status) || !isManager()
})

async function mounted() {
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

async function save({values, valid}: {values: any, valid: boolean}) {
  if (invoiceNomenclatures.value.length === 0) {
    toast.add({severity: 'error', summary: 'Ошибка', detail: 'Нужно добавить хотя бы одну номенклатуру', life: 3000})
    return
  }
  if (!valid) return
  disabled.value = true
  values.nomenclatures = invoiceNomenclatures.value
  try {
    if (props.invoice?.id) {
      await invoiceService.update(props.invoice.id, values)
    } else {
      await invoiceService.create(values)
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
    <Form v-slot="$form" :resolver="resolver" :initial-values="invoice" @submit="save" method="post" autocomplete="off">
      <div class="grid gap-8 grid-cols-3 mt-5">
        <div class="col-span-3">
          <FloatLabel>
            <Select emptyMessage="Пусто" required id="org" class="w-full" name="org" :disabled="nDisabled"
                    :options="organizations" option-value="uuid" option-label="name"/>
            <label for="org" class="text-sm">Грузополучатель</label>
          </FloatLabel>
        </div>
        <div class="col-span-3">
          <FloatLabel>
            <Select @update:model-value="(value: string) => {
                      $form.address.value = specifications?.find((s: Specification) => s.uuid === value)?.delivery_address
                    }" emptyMessage="Пусто" required id="specification" class="w-full" name="specification"
                    :disabled="nDisabled" :options="specifications" option-value="uuid" option-label="name"/>
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
                        placeholder="Выберите номенклатуру" v-model="data[field]" :options="nomenclatures"
                        option-value="uuid" option-label="name"/>
              </template>
            </Column>
            <Column field="value" header="Потребность">
              <template #editor="{ data, field }">
                <InputNumber :input-props="{autocomplete: 'off'}"
                             :suffix="` ${nomenclatures?.find((v: Nomenclature) => v.uuid === data?.nomenclature)?.unit}`"
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
