<script lang="ts">
import {Plus, Check, X, Pen} from "lucide-vue-next"

export default {
  name: 'Order',
  props: ['invoice'],
  components: {Plus, X, Check, Pen},
  data() {
    return {
      loading: true,
      orders: [],
      order: {},
      show_order: false,
      pivot: {},
      filters: {
        search: null,
      }
    }
  },
  async mounted() {
    await this.fetch_data()
  },
  methods: {
    rowClick(e: any) {
      this.show_order = true
      this.order = e.data
    },
    async onFilter() {
      await this.fetch_data()
    },
    async fetch_data() {
      this.loading = true
      const response = await this.$api.get(`/invoice/${this.invoice.id}/order/`, {params: this.filters})
      this.orders = response?.data
      const pivot = await this.$api.get(`/invoice/${this.invoice.id}/pivot/`)
      this.pivot = pivot?.data
      this.loading = false
    },
    confirmDelete(event: Event, data: any) {
      this.$confirm.require({
        target: event.currentTarget,
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
          await this.$api.delete(`/invoice/${this.invoice.id}/order/${data.uuid}/`)
          await this.fetch_data()
        },
      });
    }
  }
}
</script>

<template>
  <loading :loading="loading">
    <div class="flex justify-between align-items-center flex-wrap">
      <IconField class="mb-3">
        <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full"/>
        <InputIcon>
          <i class="pi pi-search cursor-pointer" @click="onFilter"/>
        </InputIcon>
      </IconField>
      <div class="flex md:flex-nowrap gap-3 flex-wrap md:w-auto w-full">
        <Button class="mb-3 w-full" @click="() => rowClick({data: {}})">
          <Plus/>
          Добавить заказ
        </Button>
      </div>
    </div>
    <DataTable size="large" :value="orders" :loading="loading" lazy rowHover>
      <Column field="created_at" header="Дата"></Column>
      <Column field="car.number" header="Авто"></Column>
      <Column field="driver.name" header="Водитель"></Column>
      <Column field="address" header="Адрес поставки"></Column>
      <Column field="nomenclature.name" header="Номенклатура"></Column>
      <Column field="per_price" header="Стоимость за ед.">
        <template #body="{data}">
          <span class="text-nowrap">{{ data.per_price }} ₽</span>
        </template>
      </Column>
      <Column field="price" header="Сумма">
        <template #body="{data}">
          <span class="text-nowrap">{{ data.price }} ₽</span>
        </template>
      </Column>
      <Column field="additive" header="Добавка">
        <template #body="{data}">
          <span class="text-nowrap">{{ data.additive }} {{ data.nomenclature.unit }}</span>
        </template>
      </Column>
      <Column field="order" header="Количество на отгрузку">
        <template #body="{data}">
          <span class="text-nowrap">{{ data.order }} {{ data.nomenclature.unit }}</span>
        </template>
      </Column>
      <Column field="fact" header="Факт">
        <template #body="{data}">
          <span v-if="data.fact" class="text-nowrap">{{ data.fact }} {{ data.nomenclature.unit }}</span>
        </template>
      </Column>
      <Column field="fact" header="Факт">
        <template #body="{data}">
          <Badge v-if="data.done" severity="success" class="p-2">
            Отгружен
          </Badge>
          <Badge v-else severity="warn" class="p-2">
            Отправлен
          </Badge>
        </template>
      </Column>
      <Column>
        <template #body="{data}">
          <div class="flex justify-center items-center">
            <Button v-if="data.done" severity="success" rounded class="size-8 !p-1">
              <Check/>
            </Button>
            <div v-else class="flex gap-2">
              <Button @click="rowClick({data: data})" severity="help" rounded class="size-8 !p-2">
                <Pen/>
              </Button>
              <Button @click="confirmDelete($event, data)" severity="danger" rounded class="size-8 !p-2">
                <X/>
              </Button>
            </div>
          </div>
        </template>
      </Column>
      <ColumnGroup type="footer" v-if="pivot.results.length > 0">
        <Row>
          <Column footer="Сумма:" :colspan="3" footer-class="!text-end font-semibold"/>
          <Column class="text-nowrap font-semibold">
            <template #footer>
              {{pivot.current_summa}} / {{pivot.summa}}
            </template>
          </Column>
          <Column :footer="pivot.results[0].name" :colspan="4" class="font-semibold"/>
          <Column class="text-nowrap font-semibold">
            <template #footer>
              {{pivot.results[0].order_current_sum}} / {{pivot.results[0].order_sum}}
            </template>
          </Column>
          <Column class="text-nowrap font-semibold">
            <template #footer>
              {{pivot.results[0].fact_current ?? 0}} / {{pivot.results[0].fact}}
            </template>
          </Column>
          <Column/>
          <Column/>
        </Row>
        <Row v-for="n in pivot.results.slice(1)">
          <Column :colspan="4"/>
          <Column :footer="n.name" :colspan="4" class="font-semibold"/>
          <Column class="text-nowrap font-semibold">
            <template #footer>
              {{n.order_current_sum}} / {{n.order_sum}}
            </template>
          </Column>
          <Column class="text-nowrap font-semibold">
            <template #footer>
              {{n.fact_current ?? 0}} / {{n.fact}}
            </template>
          </Column>
          <Column/>
          <Column/>
        </Row>
      </ColumnGroup>
      <template #empty><p class="text-center"> Заказы не найдены. </p></template>
    </DataTable>
  </loading>
  <Dialog v-model:visible="show_order" modal header="Заказ"
          :style="{ 'max-width': '700px', width: '100%'}">
    <Order v-if="show_order" :order="order" :invoice="invoice"
           @close="flag => {order = {}; show_order=false; flag ? fetch_data() : null}"/>
  </Dialog>
  <ConfirmPopup></ConfirmPopup>
</template>