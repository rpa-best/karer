<script>
import { Form } from '@primevue/forms';
import { FileImage } from 'lucide-vue-next'

export default {
    name: 'Driver',
    props: ['driver'],
    emits: ['close'],
    components: { Form, FileImage },
    data() {
        return {
            imageUrl: null,
            image: null,
            disabled: false
        };
    },
    methods: {
        onFileSelect(event) {
            const file = event.files[0];
            if (file) {
                this.image = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.imageUrl = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        },
        selectImage() {
            this.$refs.image.choose()
        },
        async save({ values }) {
            this.disabled = true
            if (this.image) {
                const formData = new FormData()
                formData.append('image', this.image)
                for (const key of Object.keys(values)) {
                    formData.append(key, values[key])
                }
                values = formData
            }
            try {
                if (this.driver.id) {
                    await this.$api.patch(`/driver/${this.driver.id}/`, values)
                } else {
                    await this.$api.post('/driver/', values)
                }
                this.$emit('close', true)
            } catch (e) { console.log(e); } finally {
                this.disabled = false
            }
        }
    }
};
</script>

<template>
    <Form :initial-values="driver" @submit="save">
        <div class="grid gap-8 grid-cols-3">
            <div class="col-span-1 text-hidden">
                <div @click="selectImage" class="flex justify-center items-center bg-surface-200 rounded-xl h-full">
                    <img :src="imageUrl || driver.image" v-if="imageUrl || driver.image" class="object-contain" />
                    <FileImage v-else class="text-gray-500 size-8" />
                </div>
                <FileUpload ref="image" mode="basic" name="image" accept="image/*" @select="onFileSelect"/>
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
                            <InputText required id="phone" style="width: 100%" name="phone" :disabled="disabled" />
                            <label for="phone" style="font-size: 12px">Номер телефона</label>
                        </FloatLabel>
                    </div>
                </div>
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
