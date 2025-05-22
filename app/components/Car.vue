<script setup lang="ts">
import { FileImage } from 'lucide-vue-next'
import { ref } from 'vue'
import type { Car } from '~/types/car'
import type { FormSubmitEvent } from '@primevue/forms'
import { CarService } from '~/services'

const props = defineProps<{
    car: Car | undefined
}>()

const emit = defineEmits<{
    close: [success?: boolean]
}>()

const imageUrl = ref<string | null>(null)
const image = ref<File | null>(null)
const disabled = ref(false)
const imageRef = ref()
const carService = new CarService()

const onFileSelect = (event: any) => {
    const file = event.files[0]
    if (file) {
        image.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
            imageUrl.value = e.target?.result as string
        }
        reader.readAsDataURL(file)
    }
}

const selectImage = () => {
    imageRef.value.choose()
}

const save = async ({ values }: FormSubmitEvent<Record<string, any>>) => {
    disabled.value = true
    try {
        let formData: FormData | Car = values as Car
        if (image.value) {
            formData = new FormData()
            formData.append('image', image.value)
            for (const key of Object.keys(values)) {
                formData.append(key, String(values[key as keyof Car]))
            }
        }
        if (props.car?.id) {
            await carService.update(props.car.id, formData)
        } else {
            await carService.create(formData)
        }
        emit('close', true)
    } finally {
        disabled.value = false
    }
}
</script>

<template>
    <Form :initial-values="car" @submit="save">
        <div class="grid gap-8 grid-cols-3">
            <div class="col-span-1 text-hidden">
                <div @click="selectImage" class="flex justify-center items-center bg-surface-200 rounded-xl h-full">
                    <img :src="imageUrl || car?.image" v-if="imageUrl || car?.image" class="object-contain" />
                    <FileImage v-else class="text-gray-500 size-8" />
                </div>
                <FileUpload ref="imageRef" mode="basic" name="image" accept="image/*" @select="onFileSelect"/>
            </div>
            <div class="col-span-2 mt-5">
                <div class="grid grid-cols-2 gap-8">
                    <div class="col-span-2">
                        <FloatLabel>
                            <InputText required id="number" style="width: 100%" name="number" :disabled="disabled" />
                            <label for="number" style="font-size: 12px">Номер</label>
                        </FloatLabel>
                    </div>
                    <div class="col-span-1">
                        <FloatLabel>
                            <InputText required id="marka" style="width: 100%" name="marka" :disabled="disabled" />
                            <label for="marka" style="font-size: 12px">Марка</label>
                        </FloatLabel>
                    </div>
                    <div class="col-span-1">
                        <FloatLabel>
                            <InputText required id="model" style="width: 100%" name="model" :disabled="disabled" />
                            <label for="model" style="font-size: 12px">Модель</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
            <div class="col-span-3">
                <FloatLabel>
                    <InputText required id="vin" style="width: 100%" name="vin" :disabled="disabled" />
                    <label for="vin" style="font-size: 12px">VIN-номер</label>
                </FloatLabel>
            </div>
            <div class="col-span-3 flex align-items-center">
                <Checkbox inputId="not_weight" id="not_weight" name="not_weight" :disabled="disabled" binary />
                <label for="weigh" class="ml-2">Не взвешивать</label>
            </div>
        </div>
        <div class="flex flex-row gap-3 mt-2">
            <Button @click="$emit('close')" class="w-full" severity="secondary">Отменить</Button>
                <Button :disabled="disabled" :loading="disabled" type="submit" class="w-full">Сохранить</Button>
            </div>
        </Form>
</template>

<style>
.text-hidden > .p-fileupload {
    display: none;
}
</style>
