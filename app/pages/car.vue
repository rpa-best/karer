<script setup lang="ts">
import {Pen, Plus} from "lucide-vue-next"
import type { Car } from "~/types/onec"
import { CarService } from "~/services"
import type { DefaultQueryParams } from '~/types'
import { useQuery } from '@tanstack/vue-query'

const filters = ref<DefaultQueryParams>({})
const car = ref<Car | null>(null)
const show_car = ref(false)
const carService = new CarService()

const {data: cars, isFetching, refetch} = useQuery({
  queryKey: computed(() => ['cars', filters.value]),
  queryFn: async () => await carService.list<Car[]>(filters.value)
})

const rowClick = (data: Car | null) => {
    show_car.value = true
    car.value = data
}

const onFilter = async () => {
    await refetch()
}

</script>

<template>
    <Loading :loading="isFetching">
        <div class="flex justify-between align-items-center flex-wrap">
            <h2 style="font-size: 24px; font-weight: bold" class="mb-3">Автомобили</h2>
            <div class="flex md:flex-nowrap gap-3 flex-wrap md:w-auto w-full">
                <IconField class="w-full mb-3">
                    <InputText placeholder="Поиск" v-model="filters.search" @keydown.enter="onFilter" class="w-full" />
                    <InputIcon>
                        <i class="pi pi-search cursor-pointer" @click="onFilter" />
                    </InputIcon>
                </IconField>
                <Button class="mb-3 w-full" @click="() => rowClick(null)">
                    <Plus />
                    Добавить автомобиль
                </Button>
            </div>
        </div>
        <Card>
            <template #content>
                <DataTable size="large" :value="cars" lazy :loading="isFetching" rowHover>
                    <Column field="reg_number" header="Номер" style="font-weight: 600"></Column>
                    <Column field="brand" header="Марка" style="font-weight: 600"></Column>
                    <Column field="name" header="Модель" style="font-weight: 600"></Column>
                    <column>
                      <template #body="{data}">
                        <Button @click="rowClick(data)" severity="help" rounded class="size-8 !p-2">
                          <Pen />
                        </Button>
                      </template>
                    </column>
                    <template #empty> <p class="text-center"> Машины не найдены. </p></template>
                </DataTable>
            </template>
        </Card>
    </Loading>
    <Dialog v-model:visible="show_car" @close="car = null" modal header="Изменить автомобиль" :style="{ 'max-width': '500px', width: '100%' }">
        <Car v-if="show_car" :car="car" @close="(flag: boolean) => {car = null; show_car=false; flag ? refetch() : null}" />
    </Dialog>
</template>

