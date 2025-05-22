<template>
    <NuxtLink :to="p('/')" class="flex flex-row items-center">
        <img class="mr-2" src="/favicon.ico" width="30"/>
        <span v-if="!noLabel" class="text-lg text-gray-700">
            <p class="mb-0 text-xl font-bold text-transparent bg-clip-text bg-gradient-to-br from-[#00d8a5] to-[#8cd66a]"
                style="line-height: 16px;">Career</p>
        </span>
    </NuxtLink>
</template>

<script lang="ts" setup>
defineProps<{
  noLabel?: boolean
}>()

const p = (value: string) => useLocalePath()(value)
</script>