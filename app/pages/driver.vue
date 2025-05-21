<script setup lang="ts">
import {Pen, Plus} from "lucide-vue-next"
import { ref, onMounted } from 'vue'
import type {DriverParams} from "@/store/driver"
import { useDriver } from "@/store/driver"
import type { Driver } from "~/types/driver"

const loading = ref(true)
const driver = ref<Driver | null>(null)
const show_driver = ref(false)
const drivers = useDriver()
const filters = ref<DriverParams>({
  search: null
})

const rowClick = (data: Driver | null = null) => {
  show_driver.value = true
  driver.value = data
}

const fetch_data = async () => {
  loading.value = true
  await drivers.fetchDrivers(filters.value)
  loading.value = false
}

const onFilter = async () => {
  await fetch_data()
}

onMounted(async () => {
  await fetch_data()
})
</script>

<template>
  <Loading :loading="loading">
    <div class="flex justify-between align-items-center flex-wrap">
      <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Водители</h2>
      <div class="flex gap-3 md:flex-nowrap flex-wrap md:w-auto w-full">
        <IconField class="w-full">
          <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full"/>
          <InputIcon>
            <i class="pi pi-search cursor-pointer" @click="onFilter"/>
          </InputIcon>
        </IconField>
        <Button class="mb-3 w-full" @click="() => rowClick()">
          <Plus/>
          Добавить водителя
        </Button>
      </div>
    </div>
    <Card>
      <template #content>
        <DataTable size="large" :value="drivers.drivers" :loading="loading" lazy rowHover>
          <Column field="id" header="ID" style="font-weight: 600"></Column>
          <Column field="name" header="ФИО" style="font-weight: 600"></Column>
          <Column field="phone" header="Телефон" style="font-weight: 600"></Column>
          <column>
            <template #body="{data}">
              <Button @click="rowClick(data)" severity="help" rounded class="size-8 !p-2">
                <Pen/>
              </Button>
            </template>
          </column>
          <template #empty><p class="text-center"> Водители не найдены. </p></template>
        </DataTable>
      </template>

    </Card>
  </Loading>
  <Dialog v-model:visible="show_driver" @close="driver=null" modal header="Изменить водителя"
          :style="{ 'max-width': '500px', width: '100%'}">
    <Driver v-if="show_driver" :driver="driver"
            @close="(flag: boolean) => {driver = null; show_driver=false; flag ? fetch_data() : null}"/>
  </Dialog>
</template>