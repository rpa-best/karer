<template>
  <button @click="toggle"
          class="hidden md:flex gap-3 items-center w-full outline-none bg-transparent p-2.5 rounded-full text-gray-600  hover:bg-gray-100">
    <Avatar v-if="user.id" :label="user.first_name[0]" class="cursor-pointer" shape="circle"/>
    <CircleUserRound class="size-7 text-gray-700 cursor-pointer" v-else/>
    <p class="font-bold">{{ user.first_name }} {{ user.last_name }}</p>
  </button>
  <Popover ref="user">
    <div class="flex flex-row">
      <Menu :model="items" class="!border-0">
        <template #start>
          <button v-if="user.id" v-ripple
                  class="relative overflow-hidden w-full border-0 bg-transparent flex items-center p-2 pl-4 hover:bg-surface-100 rounded-none cursor-pointer transition-colors duration-200">
            <Avatar :label="user.first_name[0]" class="mr-2 cursor-pointer" shape="circle" @click="toggle"/>
            <span class="inline-flex flex-col items-start">
                            <span class="font-bold">{{ user.first_name }} {{ user.last_name }}</span>
                        </span>
          </button>
        </template>
        <template #item="{ item, props }">
          <a v-ripple class="flex items-center" v-bind="props.action">
            <component :is="item.icon"/>
            <span>{{ $t(item.label) }}</span>
          </a>
        </template>
      </Menu>
    </div>
  </Popover>
</template>
<script>
import {useUser} from "@/store/user"

import {LogOut, LogIn, CircleUserRound} from 'lucide-vue-next'

export default {
  data() {
    return {}
  },
  components: {LogOut, CircleUserRound},
  async mounted() {
    await useUser().fetch_user()
  },
  computed: {
    user: () => useUser().user,
    items() {
      return [
        {
          label: this.user?.id ? this.$t('Выйти') : this.$t('Войти'),
          icon: this.user?.id ? LogOut : LogIn,
          command: () => {
            if (this.user?.id) {
              useUser().logout()
            } else {
              useUser().login()
            }

          }
        }
      ]
    }
  },
  methods: {
    toggle(event) {
      return this.$refs.user.toggle(event)
    }
  }
}
</script>