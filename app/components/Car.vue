<script setup lang="ts">
import { FileImage } from 'lucide-vue-next'
import { ref } from 'vue'
import type { Car } from '~/types/onec'
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

// Машина из 1С — поля из 1С только для чтения
const isFromOnec = computed(() => !!props.car?.sender)

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
        if (props.car?.uuid) {
            await carService.update(props.car.uuid, formData)
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
            <!-- Фото -->
            <div class="col-span-1 text-hidden">
                <div @click="selectImage" class="flex justify-center items-center bg-surface-200 rounded-xl h-full cursor-pointer hover:bg-surface-300 transition-colors">
                    <img :src="imageUrl || car?.image" v-if="imageUrl || car?.image" class="object-contain rounded-xl" />
                    <FileImage v-else class="text-gray-500 size-8" />
                </div>
                <FileUpload ref="imageRef" mode="basic" name="image" accept="image/*" @select="onFileSelect"/>
            </div>

            <div class="col-span-2 flex flex-col gap-5 mt-5">
                <!-- Поля из 1С -->
                <template v-if="isFromOnec">
                    <div class="flex flex-col gap-3 rounded-xl bg-surface-100 p-4">
                        <p class="text-xs text-muted-foreground font-semibold uppercase tracking-wide">Данные из 1С</p>
                        <div class="grid grid-cols-1 gap-3">
                            <div v-for="field in [
                                { label: 'Гос. номер', value: car?.reg_number },
                                { label: 'Марка', value: car?.brand },
                                { label: 'Модель', value: car?.name },
                                { label: 'Номер прицепа', value: car?.trailer_reg_number },
                                { label: 'Марка прицепа', value: car?.trailer_brand },
                            ]" :key="field.label" class="flex flex-col gap-1">
                                <span class="text-xs text-muted-foreground">{{ field.label }}</span>
                                <span class="text-sm font-medium">{{ field.value || '—' }}</span>
                            </div>
                            <div class="flex items-center gap-2 mt-1">
                                <i :class="car?.our_prorerty ? 'pi pi-check-circle text-green-500' : 'pi pi-times-circle text-surface-400'" class="text-base"></i>
                                <span class="text-sm text-muted-foreground">Наша собственность</span>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Редактируемые поля 1С (для машин созданных вручную) -->
                <template v-else>
                    <FloatLabel>
                        <InputText required id="reg_number" style="width: 100%" name="reg_number" :disabled="disabled" />
                        <label for="reg_number" style="font-size: 12px">Гос. номер</label>
                    </FloatLabel>
                    <div class="grid grid-cols-2 gap-4">
                        <FloatLabel>
                            <InputText id="brand" style="width: 100%" name="brand" :disabled="disabled" />
                            <label for="brand" style="font-size: 12px">Марка</label>
                        </FloatLabel>
                        <FloatLabel>
                            <InputText id="name" style="width: 100%" name="name" :disabled="disabled" />
                            <label for="name" style="font-size: 12px">Модель</label>
                        </FloatLabel>
                    </div>
                    <FloatLabel>
                        <InputText id="trailer_reg_number" style="width: 100%" name="trailer_reg_number" :disabled="disabled" />
                        <label for="trailer_reg_number" style="font-size: 12px">Номер прицепа</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="trailer_brand" style="width: 100%" name="trailer_brand" :disabled="disabled" />
                        <label for="trailer_brand" style="font-size: 12px">Марка прицепа</label>
                    </FloatLabel>
                    <div class="flex items-center gap-2">
                        <Checkbox inputId="our_prorerty" name="our_prorerty" :disabled="disabled" binary />
                        <label for="our_prorerty">Наша собственность</label>
                    </div>
                </template>

                <!-- Наши поля — всегда редактируемые -->
                <div class="flex items-center gap-2">
                    <Checkbox inputId="not_weight" name="not_weight" :disabled="disabled" binary />
                    <label for="not_weight">Не взвешивать</label>
                </div>
            </div>
        </div>

        <div class="flex flex-row gap-3 mt-4">
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
