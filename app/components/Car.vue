<script>
import { Form } from '@primevue/forms';
import { FileImage } from 'lucide-vue-next'

export default {
    name: 'Car',
    props: ['car'],
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
                if (this.car.id) {
                    await this.$api.patch(`/car/${this.car.id}/`, values)
                } else {
                    await this.$api.post('/car/', values)
                }
                this.$emit('close', true)
            } catch { } finally {
                this.disabled = false
            }
        }
    }
};
</script>

<template>
    <Form :initial-values="car" @submit="save">
        <div class="grid gap-8 grid-cols-3">
            <div class="col-span-1 text-hidden">
                <div @click="selectImage" class="flex justify-center items-center bg-surface-200 rounded-xl h-full">
                    <img :src="imageUrl || car.image" v-if="imageUrl || car.image" class="object-contain" />
                    <FileImage v-else class="text-gray-500 size-8" />
                </div>
                <FileUpload ref="image" mode="basic" name="image" accept="image/*" @select="onFileSelect"/>
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
