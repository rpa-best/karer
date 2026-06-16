<script setup lang="ts">
import { Pen, Plus } from "lucide-vue-next"
import type { ServiceCar } from '~/types/onec'
import { ServiceCarService } from '~/services'
import { useQuery } from '@tanstack/vue-query'

const car = ref<ServiceCar | null>(null)
const show_car = ref(false)
const searchQuery = ref('')
const carService = new ServiceCarService()

const { data: cars, isFetching, refetch } = useQuery({
    queryKey: computed(() => ['service-cars', searchQuery.value]),
    queryFn: async () => await carService.list<ServiceCar[]>(
        searchQuery.value ? { search: searchQuery.value } : {}
    )
})

const rowClick = (data: ServiceCar | null = null) => {
    car.value = data
    show_car.value = true
}

const onSearch = async () => {
    await refetch()
}
</script>

<template>
    <Loading :loading="isFetching">
        <div class="flex justify-between items-center flex-wrap mb-6">
            <h2 class="text-3xl font-bold">Служебные авто</h2>
            <div class="flex gap-3 md:flex-nowrap flex-wrap md:w-auto w-full mt-2">
                <IconField class="w-full">
                    <InputText placeholder="Поиск" v-model="searchQuery" @keydown.enter="onSearch" class="w-full"/>
                    <InputIcon>
                        <i class="pi pi-search cursor-pointer" @click="onSearch"/>
                    </InputIcon>
                </IconField>
                <Button class="mb-3 w-full" @click="() => rowClick()">
                    <Plus/>
                    Добавить авто
                </Button>
            </div>
        </div>

        <Card>
            <template #content>
                <DataTable size="large" :value="cars" :loading="isFetching" rowHover>
                    <Column field="reg_number" header="Номер" style="font-weight: 600"></Column>
                    <Column field="brand" header="Марка" style="font-weight: 600"></Column>
                    <Column field="name" header="Модель" style="font-weight: 600"></Column>
                    <Column>
                        <template #body="{data}">
                            <Button @click="rowClick(data)" severity="help" rounded class="size-8 !p-2">
                                <Pen/>
                            </Button>
                        </template>
                    </Column>
                    <template #empty>
                        <p class="text-center">Служебные авто не найдены.</p>
                    </template>
                </DataTable>
            </template>
        </Card>
    </Loading>

    <Dialog v-model:visible="show_car" @close="car=null" modal
            :header="car?.uuid ? 'Изменить служебное авто' : 'Добавить служебное авто'"
            :style="{ 'max-width': '500px', width: '100%'}">
        <ServiceCar v-if="show_car" :car="car ?? undefined"
                    @close="(flag: boolean) => { car = null; show_car = false; if (flag) refetch() }"/>
    </Dialog>
</template>
