<template>
  <button @click="menu?.toggle"
          class="hidden md:flex gap-3 items-center w-full outline-none bg-transparent p-2.5 rounded-full text-gray-600  hover:bg-gray-100">
    <Avatar v-if="user.user?.id" :label="user.user?.first_name[0]" class="cursor-pointer" shape="circle"/>
    <CircleUserRound class="size-7 text-gray-700 cursor-pointer" v-else/>
    <p class="font-bold">{{ user.user?.first_name }} {{ user.user?.last_name }}</p>
  </button>
  <Popover ref="menu">
    <div class="flex flex-row">
      <Menu :model="items" class="!border-0">
        <template #start>
          <button v-if="user.user?.id" v-ripple
                  class="relative overflow-hidden w-full border-0 bg-transparent flex items-center p-2 pl-4 hover:bg-surface-100 rounded-none cursor-pointer transition-colors duration-200">
            <Avatar :label="user.user?.first_name[0]" class="mr-2 cursor-pointer" shape="circle"/>
            <span class="inline-flex flex-col items-start">
                            <span class="font-bold">{{ user.user?.first_name }} {{ user.user?.last_name }}</span>
                        </span>
          </button>
        </template>
        <template #item="{ item, props }">
          <a v-ripple class="flex items-center" v-bind="props.action">
            <component v-if="item.licon" :is="item.licon"/>
            <span>{{ $t(item.label as string) }}</span>
          </a>
        </template>
      </Menu>
    </div>
  </Popover>
</template>
<script setup lang="ts">
import {useUser} from "@/store/user"
import {LogOut, LogIn, CircleUserRound} from 'lucide-vue-next'
import type { MenuItem } from 'primevue/menuitem'
import type { PopoverMethods } from 'primevue/popover'
import { UserService } from "~/services/user"

const user = useUser()
const user_service = new UserService()

const {data: user_data} = user_service.me()

watchEffect(() => {
  user.user = user_data.value
})

const menu = ref<PopoverMethods | null>(null)

const items = computed((): MenuItem[] => [
  {
    label: user.user?.id ? 'Выйти' : 'Войти',
    licon: user.user?.id ? LogOut : LogIn,
    command: () => {
      if (user.user?.id) {
        user.logout()
      } else {
        user.login()
      }
    }
  }
])


</script>