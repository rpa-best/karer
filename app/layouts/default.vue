<template>
  <Banner class="hidden md:flex" />
  <div class="relative w-full h-full p-3 gap-4 flex flex-row mx-auto">
    <AppSidebar class="w-[400px] hidden md:flex" />
    <div class="bg-surface-50 rounded-lg p-3 w-full md:h-auto">
      <slot v-if="auth" />
      <div v-else class="h-screen flex items-center flex-col pt-24">
        <h2 class="text-2xl font-bold text-center">{{ $t('Вы не авторизованы') }}</h2>
        <p class="text-center">{{ $t('Для доступа к личному кабинету необходимо') }}
          <NuxtLink :href="login" class="text-primary font-bold">{{ $t('войти') }}</NuxtLink>
        </p>
      </div>
    </div>
  </div>
  <MobileNavBar />
</template>
<script>
import { token } from '~/composables';
import { LoaderCircle } from "lucide-vue-next";
import {useUser} from '@/store/user'

export default {
  data() {
    return {
      auth: false,
    }
  },
  components: { LoaderCircle },
  computed: {
    login: () => useUser().loginUrl()
  },
  mounted() {
    if (token.value.access) {
      this.auth = true
    }
  }
}
</script>