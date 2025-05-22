<script setup lang="ts">
import { SendHorizonal, Loader2, Check, X } from "lucide-vue-next";
import { type FormSubmitEvent } from '@primevue/forms'
import { useOrder } from "~/store/invoices";
import type { DriverComment } from "~/types/invoices";

const props = defineProps({
  order: {
    type: Object,
    required: true
  },
  invoice: {
    type: Object,
    required: true
  }
})

const loading = ref(true)
const orders = useOrder()
const chatContainer = ref<HTMLDivElement>()

const send = async ({ values }: FormSubmitEvent<Record<string, any>>) => {
  if (!values.text) return
  await orders.createDriverComment(props.invoice.id, props.order.uuid, values.text)
  await fetchComments()
}

const updateComment = async (id: number, comment: DriverComment) => {
  await orders.updateDriverComment(props.invoice.id, props.order.uuid, id, comment.text)
  comment.status = 'loading'
}

const fetchComments = async () => {
  loading.value = true
  await orders.fetchDriverComments(props.invoice.id, props.order.uuid)
  loading.value = false

  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(async () => {
  await fetchComments()
})

defineEmits(['close'])
</script>

<template>
  <Loading :loading="loading">
    <div class="min-h-[300px] max-h-[600px] flex flex-col justify-between">
      <div ref="chatContainer" class="h-full w-full overflow-y-auto gap-3 flex flex-col mb-3">
        <div class="bg-surface-200 rounded-md p-2" v-for="comment in orders.driver_comments" :key="comment.id">
          <div class="text-muted-foreground mb-3">
            {{ comment.text }}
          </div>
          <div class="text-xs text-muted-foreground text-end flex flex-row justify-end gap-2 items-center">
            {{ comment.created_at }}
            <Loader2 class="animate-spin text-orange-500" v-if="comment.status === 'loading'" />
            <Check class="text-green-500" v-if="comment.status === 'ok'" />
            <X @click="updateComment(comment.id, comment)" class="text-red-500 cursor-pointer"
              v-if="comment.status === 'error'" />
          </div>
        </div>
        <div class="text-muted-foreground text-sm">
          {{ orders.driver_comments?.length }} комментариев
        </div>
      </div>
      <div v-if="!order.done">
        <Form method="post" @submit="send">
          <InputGroup>
            <InputText name="text" placeholder="Введите текст..." />
            <Button type="submit">
              <SendHorizonal />
            </Button>
          </InputGroup>
        </Form>
      </div>
    </div>
  </Loading>
</template>
