<script setup lang="ts">
import { FileImage } from 'lucide-vue-next'
import type { ServiceCar } from '~/types/onec'
import type { FormSubmitEvent } from '@primevue/forms'
import { ServiceCarService } from '~/services'
import { useToast } from 'primevue/usetoast'

const props = defineProps<{
    car: ServiceCar | undefined
}>()

const emit = defineEmits<{
    close: [success?: boolean]
}>()

const imageUrl = ref<string | null>(null)
const image = ref<File | null>(null)
const disabled = ref(false)
const deleting = ref(false)
const imageRef = ref()
const carService = new ServiceCarService()
const toast = useToast()

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

// Только цифры и английские буквы, автоматически в верхний регистр
const sanitizeRegNumber = (e: Event) => {
    const input = e.target as HTMLInputElement
    input.value = input.value.toUpperCase().replace(/[^A-Z0-9]/g, '')
}

const blockInvalidRegKey = (e: KeyboardEvent) => {
    if (e.key.length === 1 && !/[A-Za-z0-9]/.test(e.key)) e.preventDefault()
}

const save = async ({ values }: FormSubmitEvent<Record<string, any>>) => {
    disabled.value = true
    try {
        let formData: FormData | ServiceCar = values as ServiceCar
        if (image.value) {
            formData = new FormData()
            formData.append('image', image.value)
            for (const key of Object.keys(values)) {
                formData.append(key, String(values[key as keyof ServiceCar]))
            }
        }
        if (props.car?.uuid) {
            await carService.update(props.car.uuid, formData)
        } else {
            await carService.create(formData)
        }
        emit('close', true)
    } catch (e) {
        console.log(e)
    } finally {
        disabled.value = false
    }
}

const remove = async () => {
    if (!props.car?.uuid) return
    deleting.value = true
    try {
        await carService.delete(props.car.uuid)
        emit('close', true)
    } catch (e) {
        toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось удалить', life: 3000 })
    } finally {
        deleting.value = false
    }
}
</script>

<template>
    <Form :initial-values="car" @submit="save">
        <div class="grid gap-6 grid-cols-3">
            <!-- Фото -->
            <div class="col-span-1 text-hidden">
                <div @click="selectImage"
                     class="flex justify-center items-center bg-surface-200 rounded-xl h-40 cursor-pointer hover:bg-surface-300 transition-colors">
                    <img :src="imageUrl || car?.image" v-if="imageUrl || car?.image" class="object-contain rounded-xl h-full w-full" />
                    <FileImage v-else class="text-gray-500 size-8" />
                </div>
                <FileUpload ref="imageRef" mode="basic" name="image" accept="image/*" @select="onFileSelect"/>
            </div>

            <div class="col-span-2 flex flex-col gap-5 mt-2">
                <FloatLabel>
                    <InputText
                        id="reg_number"
                        style="width: 100%"
                        name="reg_number"
                        :disabled="disabled"
                        @keydown="blockInvalidRegKey"
                        @input="sanitizeRegNumber"
                    />
                    <label for="reg_number" style="font-size: 12px">Гос. номер</label>
                </FloatLabel>
                <FloatLabel>
                    <InputText id="brand" style="width: 100%" name="brand" :disabled="disabled" />
                    <label for="brand" style="font-size: 12px">Марка</label>
                </FloatLabel>
                <FloatLabel>
                    <InputText id="name" style="width: 100%" name="name" :disabled="disabled" />
                    <label for="name" style="font-size: 12px">Модель</label>
                </FloatLabel>
            </div>
        </div>

        <div class="flex flex-row gap-3 mt-6">
            <Button v-if="car?.uuid" @click="remove" :loading="deleting" :disabled="deleting || disabled"
                    severity="danger" type="button" class="w-full">
                Удалить
            </Button>
            <Button @click="$emit('close')" class="w-full" severity="secondary" type="button">Отменить</Button>
            <Button :disabled="disabled" :loading="disabled" type="submit" class="w-full">Сохранить</Button>
        </div>
    </Form>
</template>

<style>
.text-hidden > .p-fileupload {
    display: none;
}
</style>
