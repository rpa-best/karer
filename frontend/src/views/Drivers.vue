<script>
export default {
    name: 'Drivers',
    data() {
        return {
            drivers: [
                {
                    id: 1,
                    name: 'Панов Гордий Оскарович',
                    phone: '+7 (881) 791 84 48',
                }
            ]
        }
    }
}
</script>

<template>
    <div>
        <div class="flex justify-content-between align-items-center mb-3">
            <h2 style="font-size: 24px; font-weight: bold">Водители</h2>
            <IconField>
                <InputIcon>
                    <i class="pi pi-search"/>
                </InputIcon>
                <InputText placeholder="Поиск"/>
            </IconField>
        </div>
        <Card>
            <template #content>
                <DataTable size="large" :value="drivers">
                    <Column field="id" header="ID" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="name" header="ФИО" style="font-weight: 600" header-class="carsHeader"></Column>
                    <Column field="phone" header="Телефон" style="font-weight: 600" header-class="carsHeader"></Column>
                </DataTable>
            </template>

        </Card>
    </div>

</template>

<style>
.carsHeader {
    background-color: var(--surface-ground) !important;
    color: var(--surface-50) !important;
}
.carsHeader:first-child {
    border-radius: 5px 0 0 5px;
}

.carsHeader:last-child {
    border-radius: 0 5px 5px 0;
}
</style>


