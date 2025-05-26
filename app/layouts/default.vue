<template>
  <div class="relative w-full h-full p-3 gap-4 flex flex-row mx-auto">
    <AppSidebar class="w-[400px] hidden md:flex" />
    <div class="bg-surface-50 rounded-lg p-3 w-full md:h-auto">
      <slot v-if="user.isAuth()" />
      <div v-else class="h-screen flex items-center flex-col pt-24">
        <h2 class="text-2xl font-bold text-center">{{ $t('Вы не авторизованы') }}</h2>
        <p class="text-center">{{ $t('Для доступа к личному кабинету необходимо') }}
          <NuxtLink :to="user.loginUrl()" class="text-primary font-bold">{{ $t('войти') }}</NuxtLink>
        </p>
      </div>
    </div>
  </div>
  <MobileNavBar />
</template>
<script setup lang="ts">
import {useUser} from '@/store/user'
import { UserService } from '~/services/user'
import { useQuery } from '@tanstack/vue-query'

const user = useUser()

const user_service = new UserService()

useQuery({
  queryKey: ['user'],
  queryFn: async () => await user_service.me(),
  select(data) {
    user.user = data
    return data
  }
})
</script>