<script>
import {Form} from '@primevue/forms';

export default {
    name: 'Car',
    props: ["car"],
    components: {Form},
    data() {
        return {
            disabled: true,
        }
    },
}
</script>

<template>
    <Form :initial-values="car">
        <div class="grid nested-grid">
            <div class="col-3">
                <div class="car_image">
                    <i class="pi pi-image"
                       style="font-size: 24px; position: absolute; right: 10px; bottom: 10px"></i>
                </div>
            </div>
            <div class="col-9">
                <div class="grid">
                    <div class="col-12 mt-4">
                        <FloatLabel>
                            <InputText id="number" style="width: 100%" name="number" :disabled="disabled"/>
                            <label for="number" style="font-size: 12px">Номер</label>
                        </FloatLabel>
                    </div>
                    <div class="col-6 mt-3">
                        <FloatLabel>
                            <InputText id="mark" style="width: 100%" name="mark" :disabled="disabled"/>
                            <label for="mark" style="font-size: 12px">Марка</label>
                        </FloatLabel>
                    </div>
                    <div class="col-6 mt-3">
                        <FloatLabel>
                            <InputText id="model" style="width: 100%" name="model" :disabled="disabled"/>
                            <label for="model" style="font-size: 12px">Модель</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
            <div class="col-12 mt-3">
                <FloatLabel>
                    <InputText id="vin" style="width: 100%" name="vin" :disabled="disabled"/>
                    <label for="vin" style="font-size: 12px">VIN-номер</label>
                </FloatLabel>
            </div>
            <div class="col-12 flex align-items-center">
                <Checkbox inputId="not_weigh" id="not_weigh" name="not_weigh" :disabled="disabled"/>
                <label for="weigh" class="ml-2">Не взвешивать</label>
            </div>

        </div>
    </Form>
</template>

<style scoped>
.car_image {
    width: 100%;
    height: 100%;
    position: relative;
    background-color: var(--p-inputtext-disabled-background);
    border: 1px solid var(--p-inputtext-border-color);
    border-radius: var(--p-inputtext-border-radius)
}
</style>
