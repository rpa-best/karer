<script>
import {Form} from '@primevue/forms';

export default {
    name: 'Driver',
    props: ["driver"],
    components: {Form},
    data() {
        return {
            disabled: true,
        }
    },
}
</script>

<template>
    <Form :initial-values="driver">
        <div class="grid nested-grid">
            <div class="col-3">
                <div class="driver_image">
                    <i class="pi pi-image"
                       style="font-size: 24px; position: absolute; right: 10px; bottom: 10px"></i>
                </div>
            </div>
            <div class="col-9">
                <div class="grid">
                    <div class="col-12 mt-4">
                        <FloatLabel>
                            <InputText id="name" style="width: 100%" name="name" :disabled="disabled"/>
                            <label for="name" style="font-size: 12px">ФИО</label>
                        </FloatLabel>
                    </div>
                    <div class="col-12 mt-3">
                        <FloatLabel>
                            <InputText id="phone" style="width: 100%" name="phone" :disabled="disabled"/>
                            <label for="phone" style="font-size: 12px">Телефон</label>
                        </FloatLabel>
                    </div>
                </div>
            </div>
            <div class="col-12 mt-3">
                <FloatLabel>
                    <InputText id="telegram" style="width: 100%" name="telegram" :disabled="disabled"/>
                    <label for="telegram" style="font-size: 12px">ID телеграма</label>
                </FloatLabel>
            </div>
            <div class="col-12 mt-3">
                <FloatLabel>
                    <DatePicker id="birth_date" style="width: 100%" name="birth_date" :disabled="disabled" date-format="dd.mm.yyyy"/>
                    <label for="birth_date" style="font-size: 12px">Дата рождения</label>
                </FloatLabel>
            </div>
        </div>
    </Form>
</template>

<style scoped>
.driver_image {
    width: 100%;
    height: 100%;
    position: relative;
    background-color: var(--p-inputtext-disabled-background);
    border: 1px solid var(--p-inputtext-border-color);
    border-radius: var(--p-inputtext-border-radius)
}
</style>
