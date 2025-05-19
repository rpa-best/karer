<script lang="ts">
import { Bell, CheckCheck, X, Check, Info } from "lucide-vue-next";
import {useNotification, type Notification} from "~/store/notifications.js";
import {NotificationSocket} from "./websocket"

export default {
  components: { Bell, CheckCheck, X, Check, Info },
  data() {
    return {
      loading: true,
      open: false,
      notification: useNotification(),
      socket: null
    }
  },
  async mounted() {
    await this.fetch_data()

    const socket = new NotificationSocket()
    console.log(socket)
  },
  methods: {
    format(value: string) {
      return value
      // return formatDistanceToNow(new Date(value), { addSuffix: true, locale: ru })
    },
    async fetch_data() {
      this.loading = true
      await this.notification.fetchData()
      this.loading = false
    },
    async select(item: Notification) {
      if (!item.read) {
        await this.notification.read(item.id)
        item.read = true
      }
      await this.$router.push(item.redirect_url)
    },
    async allCheck() {
      if (this.notification.items.unread > 0) {
        await this.notification.readAll()
        await this.fetch_data()
      }
    }
  }
}
</script>

<template>
  <button id="notifications" @click="open = true" class="w-full h-fit md:w-auto px-4 relative md:px-2 flex flex-row items-center outline-none bg-transparent p-2.5 md:rounded-full rounded-lg text-gray-600  hover:bg-gray-100">

    <OverlayBadge v-if="notification.items.unread" :value="notification.items.unread" severity="danger" size="small">
      <Bell />
    </OverlayBadge>
    <Bell v-else />
    <div class="ml-4 md:hidden">Уведомление</div>
  </button>
  <Drawer position="right" v-model:visible="open" :header="'Уведомление'">
    <template #header>
      <div class="flex flex-row justify-between items-center w-full">
        {{ 'Уведомление' }}
        <button class="cursor-pointer hover:bg-gray-100 p-2 rounded-full" @click="allCheck" >
          <CheckCheck  />
        </button>
      </div>
    </template>
    <Loading :loading="loading">
      <div class="flex-1 flex flex-col gap-2 pt-0">
        <TransitionGroup name="list" appear>
          <Button v-for="item of notification.items.results" :key="item.id" outlined
                  class="flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent"
                  @click="select(item)" :severity="item.severity">
            <div class="flex w-full flex-col gap-1">
              <div class="flex items-center">
                <Button :severity="item.severity" rounded class="p-1">
                  <X v-if="item.severity === 'danger'" />
                  <Info v-if="item.severity === 'info'" />
                  <Check v-if="item.severity === 'success'" />
                </Button>
                <div class="flex items-center gap-2 ml-2">
                  <div class="font-semibold">
                    {{ item.label }}
                  </div>
                  <span v-if="!item.read" class="flex h-2 w-2 rounded-full bg-blue-600" />
                </div>
              </div>

              <div class="text-xs font-medium">
                {{ item.message }}
              </div>
              <div v-if="item.created_at" class="ml-auto text-xs text-muted-foreground">
                {{ format(item.created_at) }}
              </div>
            </div>
          </Button>
        </TransitionGroup>
      </div>
    </Loading>
  </Drawer>
</template>