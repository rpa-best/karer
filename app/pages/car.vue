<script setup lang="ts">
import {Pen, Plus} from "lucide-vue-next"
import { ref, onMounted } from 'vue'
import type { Car } from "~/types/car"
import { CarService } from "~/services"
import type { DefaultQueryParams } from '~/types'

const loading = ref(true)
const car = ref<Car | null>(null)
const show_car = ref(false)
const carService = new CarService()
const cars = ref<Car[]>([])
const filters = ref<DefaultQueryParams>({})

const rowClick = (data: Car | null) => {
    show_car.value = true
    car.value = data
}

const fetch_data = async () => {
    loading.value = true
    cars.value = await carService.list(filters.value)
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
                <DataTable size="large" :value="cars" lazy :loading="loading" rowHover>
                    <Column field="number" header="Номер" style="font-weight: 600"></Column>
                    <Column field="marka" header="Марка" style="font-weight: 600"></Column>
                    <Column field="model" header="Модель" style="font-weight: 600"></Column>
                    <Column field="vin" header="VIN-Номер" style="font-weight: 600"></Column>
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
        <Car v-if="show_car" :car="car" @close="(flag: boolean) => {car = null; show_car=false; flag ? fetch_data() : null}" />
    </Dialog>
</template>

