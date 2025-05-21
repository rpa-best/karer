<template>
  <div class="bg-gradient-to-tl from-green-400 to-indigo-900 px-6 py-20 md:px-12 lg:px-20 h-screen flex flex-col justify-center items-center">
    <div class="bg-surface-0 dark:bg-surface-900 p-6 shadow rounded-border max-w-[500px] w-full lg:w-6/12 mx-auto">
      <div class="mb-8">
        <Logo class="w-32 mx-auto logo-spin" />
      </div>

      <!--      <div class="flex flex-col gap-3">-->
      <!--        <TelegramAuthButton />-->
      <!--        <GoogleAuthButton />-->
      <!--      </div>-->

      <!--      <div class="w-full flex items-center justify-between py-5">-->
      <!--        <hr class="w-full border-gray-500">-->
      <!--        <p class="text-base font-medium leading-4 px-2.5 text-gray-400">{{$t('ИЛИ')}}</p>-->
      <!--        <hr class="w-full border-gray-500">-->
      <!--      </div>-->
      <Loading :loading="loading" class="!max-h-[100px]">
        <Form @submit="auth" method="post">
          <label for="email" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Почта</label>
          <InputText id="email" name="email" type="email" placeholder="Введите почту" class="w-full mb-4" required/>

          <label for="password" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Пароль</label>
          <Password id="password" name="password" type="password" placeholder="Введите пароль" class="w-full mb-4" fluid :feedback="false" required/>

          <Button type="submit" label="Продолжить" icon="pi pi-user !text-xl !leading-none" class="w-full"/>
        </Form>
      </Loading>

    </div>
  </div>

</template>
<script setup lang="ts">
import { useUser } from '@/store/user'
import type { UserLogin } from '~/types/user'
import {Form, type FormSubmitEvent} from '@primevue/forms'

definePageMeta({
  layout: false
})

const loading = ref(false)

const user = useUser()

async function auth(event: FormSubmitEvent<Record<string, any>>) {
  loading.value = true
  try {
    await user.auth(event.values as UserLogin)
    user.redirect()
  } catch {
    loading.value = false
  }
}
</script>
