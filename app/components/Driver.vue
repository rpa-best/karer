<script setup lang="ts">
import { FileImage } from 'lucide-vue-next'
import { ref } from 'vue'
import type { Driver } from '~/types/onec'
import type { FormSubmitEvent } from '@primevue/forms'
import { DriverService } from '~/services'

const props = defineProps<{
    driver: Driver | undefined
}>()

const emit = defineEmits<{
    close: [success?: boolean]
}>()

const imageUrl = ref<string | null>(null)
const image = ref<File | null>(null)
const disabled = ref(false)
const imageRef = ref()
const driverService = new DriverService()

// Водитель из 1С — поля из 1С только для чтения
const isFromOnec = computed(() => !!props.driver?.sender)

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
        let formData: FormData | Driver = values as Driver
        if (image.value) {
            formData = new FormData()
            formData.append('image', image.value)
            for (const key of Object.keys(values)) {
                formData.append(key, String(values[key as keyof Driver]))
            }
        }
        if (props.driver?.uuid) {
            await driverService.update(props.driver.uuid, formData)
        } else {
            await driverService.create(formData)
        }
        emit('close', true)
    } catch (e) {
        console.log(e)
    } finally {
        disabled.value = false
    }
}
</script>

<template>
    <Form :initial-values="driver" @submit="save">
        <div class="grid gap-8 grid-cols-3">
            <!-- Фото -->
            <div class="col-span-1 text-hidden">
                <div @click="selectImage" class="flex justify-center items-center bg-surface-200 rounded-xl h-full cursor-pointer hover:bg-surface-300 transition-colors">
                    <img :src="imageUrl || driver?.image" v-if="imageUrl || driver?.image" class="object-contain rounded-xl" />
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
                                { label: 'ФИО', value: driver?.name },
                                { label: 'ИНН', value: driver?.inn },
                                { label: 'Телефон', value: driver?.phone_number },
                                { label: 'Профессия', value: driver?.job_title },
                                { label: 'Серия ВУ', value: driver?.drivers_license_series },
                                { label: 'Номер ВУ', value: driver?.drivers_license_number },
                            ]" :key="field.label" class="flex flex-col gap-1">
                                <span class="text-xs text-muted-foreground">{{ field.label }}</span>
                                <span class="text-sm font-medium">{{ field.value || '—' }}</span>
                            </div>
                        </div>
                    </div>
                </template>

                <!-- Редактируемые поля 1С (для водителей, созданных вручную) -->
                <template v-else>
                    <FloatLabel>
                        <InputText required id="name" style="width: 100%" name="name" :disabled="disabled" />
                        <label for="name" style="font-size: 12px">ФИО</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="inn" style="width: 100%" name="inn" :disabled="disabled" />
                        <label for="inn" style="font-size: 12px">ИНН</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="phone_number" style="width: 100%" name="phone_number" :disabled="disabled" />
                        <label for="phone_number" style="font-size: 12px">Номер телефона</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="job_title" style="width: 100%" name="job_title" :disabled="disabled" />
                        <label for="job_title" style="font-size: 12px">Профессия</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="drivers_license_series" style="width: 100%" name="drivers_license_series" :disabled="disabled" />
                        <label for="drivers_license_series" style="font-size: 12px">Серия ВУ</label>
                    </FloatLabel>
                    <FloatLabel>
                        <InputText id="drivers_license_number" style="width: 100%" name="drivers_license_number" :disabled="disabled" />
                        <label for="drivers_license_number" style="font-size: 12px">Номер ВУ</label>
                    </FloatLabel>
                </template>

                <!-- Telegram ID — всегда редактируемый -->
                <FloatLabel>
                    <InputText id="telegram_id" style="width: 100%" name="telegram_id" :disabled="disabled" />
                    <label for="telegram_id" style="font-size: 12px">Telegram ID</label>
                </FloatLabel>
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
