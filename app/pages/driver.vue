<script setup lang="ts">
import {Pen, Plus} from "lucide-vue-next"
import type { Driver } from "~/types/onec"
import type { DefaultQueryParams } from '~/types'
import { DriverService } from '~/services'
import { useQuery } from '@tanstack/vue-query'

const filters = ref<DefaultQueryParams>({})
const driver = ref<Driver | null>(null)
const show_driver = ref(false)
const driverService = new DriverService()

const {data: drivers, isFetching, refetch} = useQuery({
  queryKey: computed(() => ['drivers', filters.value]),
  queryFn: async () => await driverService.list<Driver[]>(filters.value)
})

const rowClick = (data: Driver | null = null) => {
  show_driver.value = true
  driver.value = data
}

const onFilter = async () => {
  await refetch()
}
</script>

<template>
  <Loading :loading="isFetching">
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
        <DataTable size="large" :value="drivers" :loading="isFetching" lazy rowHover>
          <Column field="inn" header="ИНН" style="font-weight: 600"></Column>
          <Column field="name" header="ФИО" style="font-weight: 600"></Column>
          <Column field="phone_number" header="Телефон" style="font-weight: 600"></Column>
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
            @close="(flag: boolean) => {driver = null; show_driver=false; flag ? refetch() : null}"/>
  </Dialog>
</template>