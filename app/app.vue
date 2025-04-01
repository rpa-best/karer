<template>
  <Toast />
  <div class="pb-[85px] md:pb-0 h-full">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
  <div v-if="loader().loading" class="absolute top-0 left-0 w-full h-full bg-white z-[998]">
    <Loader />
  </div>
</template>

<script setup>
import { token } from './composables'
import loader from "~/store/loader";

const colorMode = useColorMode();
colorMode.preference = 'light';

useHead({
  title: 'Career',
  meta: [
    { name: 'description', content: '' },
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'apple-mobile-web-app-capable', content: 'yes' },
    { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
    { name: 'apple-mobile-web-app-title', content: 'Career' },
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' },
  ]
})

onMounted(async () => {
  if (useRoute().query.access) token.value.access = useRoute().query.access
  if (useRoute().query.refresh) token.value.refresh = useRoute().query.refresh
})
</script>
<style>
html {
  color-scheme: light;
}
</style>
