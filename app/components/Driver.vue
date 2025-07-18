<script setup lang="ts">
import { FileImage } from 'lucide-vue-next'
import { ref } from 'vue'
import type { Driver } from '~/types/onec'
import type { FormSubmitEvent } from '@primevue/forms'
import { DriverService } from '~/services'
const props =defineProps<{
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
            <div class="col-span-1 text-hidden">
                <div @click="selectImage" class="flex justify-center items-center bg-surface-200 rounded-xl h-full">
                    <img :src="imageUrl || driver?.image" v-if="imageUrl || driver?.image" class="object-contain" />
                    <FileImage v-else class="text-gray-500 size-8" />
                </div>
                <FileUpload ref="imageRef" mode="basic" name="image" accept="image/*" @select="onFileSelect"/>
            </div>
            <div class="col-span-2 mt-5">
                <div class="grid grid-cols-2 gap-8">
                    <div class="col-span-2">
                        <FloatLabel>
                            <InputText required id="name" style="width: 100%" name="name" :disabled="disabled" />
                            <label for="name" style="font-size: 12px">ФИО</label>
                        </FloatLabel>
                    </div>
                    <div class="col-span-2">
                        <FloatLabel>
                            <InputText required id="inn" style="width: 100%" name="inn" :disabled="disabled" />
                            <label for="inn" style="font-size: 12px">Номер телефона</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputText required id="phone_number" style="width: 100%" name="phone_number" :disabled="disabled" />
                    <label for="phone_number" style="font-size: 12px">Номер телефона</label>
                </FloatLabel>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputText required id="job_title" style="width: 100%" name="job_title" :disabled="disabled" />
                    <label for="job_title" style="font-size: 12px">Профессия</label>
                </FloatLabel>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputText required id="drivers_license_series" style="width: 100%" name="drivers_license_series" :disabled="disabled" />
                    <label for="drivers_license_series" style="font-size: 12px">Серия права водителя</label>
                </FloatLabel>
            </div>
            <div class="col-span-2">
                <FloatLabel>
                    <InputText required id="drivers_license_number" style="width: 100%" name="drivers_license_number" :disabled="disabled" />
                    <label for="drivers_license_number" style="font-size: 12px">Номер права водителя</label>
                </FloatLabel>
            </div>

            <div class="col-span-3">
                <FloatLabel>
                    <InputText required id="telegram_id" style="width: 100%" name="telegram_id" :disabled="disabled" />
                    <label for="telegram_id" style="font-size: 12px">Telegram ID</label>
                </FloatLabel>
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
