<script setup lang="ts">
import { Pen, MessageCircle, Send, Trash, EllipsisVertical, Check, Plus } from "lucide-vue-next"
import { order_columns } from "~/composables"
import type { Invoice, Order, Pivot, OrderParams } from "~/types/invoices"
import { InvoiceService } from "~/services/invoice"
import { useConfirm } from "primevue/useconfirm";

const props = defineProps<{
  invoice: Invoice
}>()

const loader = ref(true)
const invoiceService = new InvoiceService()
const orders = ref<Order[]>([])
const pivot = ref<Pivot | undefined>(undefined)

const confirm = useConfirm()
const order = ref<Order | {}>({})
const show_order = ref(false)
const filters = ref<OrderParams>({})

const columns = [
  {
    field: 'uuid',
    header: 'Номер',
  },
  {
    field: 'address',
    header: 'Адрес поставки',
  },
  {
    field: 'per_price',
    header: 'Стоимость за ед.',
  },
  {
    field: 'price',
    header: 'Сумма',
  },
  {
    field: 'additive',
    header: 'Добавка',
  },
  {
    field: 'order',
    header: 'Количество на отгрузку',
  },
  {
    field: 'fact',
    header: 'Факт',
  },
]

const show_driver_comment = ref(false)
const menuItems = ref([
  {
    label: 'Параметры',
    items: [
      {
        label: 'Изменить',
        licon: Pen,
        command: () => {
          if (order.value) {
            rowClick(order.value as Order)
          }
        }
      },
      {
        label: 'Чат с водителям',
        licon: MessageCircle,
        command: () => {
          show_driver_comment.value = true
        }
      },
      {
        label: 'Отпроавить карерь',
        licon: Send,
        command: () => {
          if (order.value) {
            invoiceService.order.sendCareer(props.invoice.id, (order.value as Order).uuid)
          }
        }
      },
      {
        label: 'Удалить',
        licon: Trash,
        command: () => {
          if (order.value) confirmDelete(order.value as Order)
        }
      }
    ]
  }
])

const menu = ref()

onMounted(async () => {
  await fetch_data()
})

function rowClick(data: Order | {} = {}) {
  show_order.value = true
  order.value = data
}

async function onFilter() {
  await fetch_data()
}

async function fetch_data() {
  loader.value = true
  orders.value = await invoiceService.order.list(filters.value, { invoice_id: props.invoice.id })
  pivot.value = await invoiceService.fetchPivot(props.invoice.id, filters.value)
  loader.value = false
}

function confirmDelete(data: Order) {
  confirm.require({
    header: 'Удалить заказ',
    message: 'Вы хотите удалить эту запись?',
    rejectProps: {
      label: 'Назад',
      severity: 'secondary',
      outlined: true
    },
    acceptProps: {
      label: 'Удалить',
      severity: 'danger'
    },
    accept: async () => {
      await invoiceService.order.delete(data.uuid, {}, { invoice_id: props.invoice.id.toString() })
      await fetch_data()
    },
  })
}

function select_order(event: Event, data: Order) {
  order.value = data
  menu.value.toggle(event)
}
</script>

<template>
  <Loading :loading="loader">
    <div class="flex justify-between align-items-center flex-wrap">
      <h2 class="text-2xl font-bold">
        Заказы:
        <span class="text-primary">{{ invoice.number }}</span>
        <!-- <span v-if="orders.day_count" class="text-primary">(Отсрочка платежа осталось дней: {{orders.day_count}})</span> -->
      </h2>
      <div class="flex md:flex-nowrap gap-3 flex-wrap md:w-auto w-full">
        <IconField class="mb-3 w-full">
          <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter"
            class="w-full min-w-[200px]" />
          <InputIcon>
            <i class="pi pi-search cursor-pointer" @click="onFilter" />
          </InputIcon>
        </IconField>
        <MultiSelect v-model="order_columns" display="chip" :options="columns" option-value="field" optionLabel="header"
          placeholder="Выберите столбцы..." :maxSelectedLabels="0" class="mb-3 w-full md:w-80"
          selectedItemsLabel="{0} столбцы выбраны" />
        <Button class="mb-3 w-full" @click="() => rowClick()">
          <Plus />
          Добавить заказ
        </Button>
      </div>
    </div>
    <DataTable size="large" :value="orders" :loading="loader" rowHover responsive-layout="scroll">
      <Column field="uuid" header="Номер" class="text-nowrap" v-if="order_columns.includes('uuid')">
        <template #body="{ data }">
          <NuxtLink class="text-nowrap text-primary font-semibold" :to="`/orders/${data.uuid}`">{{ data.uuid }}</NuxtLink>
        </template>
      </Column>
      <Column field="created_at" header="Дата"></Column>
      <Column field="car.number" header="Авто"></Column>
      <Column field="driver.name" header="Водитель"></Column>
      <Column field="nomenclature.name" header="Номенклатура" class="text-nowrap"></Column>
      <Column v-if="order_columns.includes('address')" field="address" header="Адрес поставки"></Column>
      <Column v-if="order_columns.includes('per_price')" field="per_price" header="Стоимость за ед.">
        <template #body="{ data }">
          <span class="text-nowrap">{{ data.per_price }} ₽</span>
        </template>
      </Column>
      <Column v-if="order_columns.includes('price')" field="price" header="Сумма">
        <template #body="{ data }">
          <span class="text-nowrap">{{ data.price }} ₽</span>
        </template>
      </Column>
      <Column v-if="order_columns.includes('additive')" field="additive" header="Добавка">
        <template #body="{ data }">
          <span class="text-nowrap">{{ data.additive }} {{ data.nomenclature.unit }}</span>
        </template>
      </Column>
      <Column v-if="order_columns.includes('order')" field="order" header="Количество на отгрузку">
        <template #body="{ data }">
          <span class="text-nowrap">{{ data.order }} {{ data.nomenclature.unit }}</span>
        </template>
      </Column>
      <Column v-if="order_columns.includes('fact')" field="fact" header="Факт">
        <template #body="{ data }">
          <span v-if="data.fact" class="text-nowrap">{{ data.fact }} {{ data.nomenclature.unit }}</span>
        </template>
      </Column>
      <Column field="fact" header="Статус">
        <template #body="{ data }">
          <Badge v-if="data.done" severity="success" class="p-2">
            Отгружен
          </Badge>
          <Badge v-else severity="warn" class="p-2">
            Отправлен
          </Badge>
        </template>
      </Column>
      <Column>
        <template #body="{ data }">
          <div class="flex justify-center items-center">
            <Button v-if="data.done" severity="success" rounded class="size-8 !p-1">
              <Check />
            </Button>
            <div v-else class="flex gap-2">
              <Button @click="(e: Event) => select_order(e, data)" aria-haspopup="true" aria-controls="overlay_menu"
                rounded class="size-8 !p-2">
                <EllipsisVertical />
              </Button>
            </div>
          </div>
        </template>
      </Column>
      <ColumnGroup type="footer" v-if="(pivot?.results?.length ?? 0) > 0">
        <Row>
          <Column v-if="order_columns.includes('uuid')"></Column>
          <Column v-if="invoice.type === 'limit'" footer="Лимит:" :colspan="2" footer-class="!text-end font-semibold" />
          <Column v-if="invoice.type === 'limit'" class="text-nowrap font-semibold">
            <template #footer>
              {{ pivot?.current_summa ?? 0 }} / {{ pivot?.summa }}
            </template>
          </Column>
          <Column v-else :colspan="4" />
          <Column :footer="pivot?.results[0].name" class="font-semibold" />
          <Column v-if="order_columns.includes('address')"></Column>
          <Column v-if="order_columns.includes('per_price')"></Column>
          <Column v-if="order_columns.includes('price')"></Column>
          <Column v-if="order_columns.includes('additive')"></Column>
          <Column v-if="order_columns.includes('order')" class="text-nowrap font-semibold">
            <template #footer>
              {{ pivot?.results[0].order_current_sum ?? 0 }} / {{ pivot?.results[0].order_sum }}
            </template>
          </Column>
          <Column v-if="order_columns.includes('fact')" class="text-nowrap font-semibold">
            <template #footer>
              {{ pivot?.results[0].fact_current ?? 0 }} / {{ pivot?.results[0].fact }}
            </template>
          </Column>
          <Column />
          <Column />
        </Row>
        <Row v-for="n in pivot?.results.slice(1)">
          <Column v-if="order_columns.includes('uuid')"></Column>
          <Column :colspan="3" />
          <Column :footer="n.name" class="font-semibold text-nowrap" />
          <Column v-if="order_columns.includes('address')"></Column>
          <Column v-if="order_columns.includes('per_price')"></Column>
          <Column v-if="order_columns.includes('price')"></Column>
          <Column v-if="order_columns.includes('additive')"></Column>
          <Column v-if="order_columns.includes('order')" class="text-nowrap font-semibold">
            <template #footer>
              {{ n.order_current_sum ?? 0 }} / {{ n.order_sum }}
            </template>
          </Column>
          <Column v-if="order_columns.includes('fact')" class="text-nowrap font-semibold">
            <template #footer>
              {{ n.fact_current ?? 0 }} / {{ n.fact }}
            </template>
          </Column>
          <Column />
          <Column />
        </Row>
      </ColumnGroup>
      <template #empty>
        <p class="text-center"> Заказы не найдены. </p>
      </template>
    </DataTable>
  </Loading>
  <Dialog v-model:visible="show_order" modal :header="`Заказ`" :style="{ 'max-width': '700px', width: '100%' }">
    <Order :order="order" :invoice="invoice"
      @close="(flag: boolean | undefined) => { order = {}; show_order = false; flag ? fetch_data() : null }" />
  </Dialog>
  <ConfirmDialog></ConfirmDialog>

  <Menu ref="menu" id="overlay_menu" :model="menuItems" :popup="true">
    <template #itemicon="{ item }">
      <component v-if="item.licon" :is="item.licon" :size="14" />
    </template>
  </Menu>

  <Dialog v-model:visible="show_driver_comment" modal header="Чат с водителям"
    :style="{ 'max-width': '700px', width: '100%' }">
    <DriverComment v-if="order" :order="order" :invoice="invoice"
      @close="order = {}; show_driver_comment = false" />
  </Dialog>
</template>