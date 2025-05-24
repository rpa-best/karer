<script setup lang="ts">
import { SendHorizonal, Loader2, Check, X, RefreshCcw } from "lucide-vue-next";
import { type FormSubmitEvent } from '@primevue/forms'
import type { DriverComment } from "~/types/invoices";
import { InvoiceService } from '~/services/invoice'
import { useQuery } from "@tanstack/vue-query";

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

const invoiceService = new InvoiceService()

const {data: comments, isFetching, refetch} = useQuery({
  queryKey: ['driver-comments', props.invoice.id, props.order.uuid],
  queryFn: async () => await invoiceService.order.driverComment.list<DriverComment[]>({}, {invoice_id: props.invoice.id, order_id: props.order.uuid})
})

const chatContainer = ref<HTMLDivElement>()

const send = async ({ values }: FormSubmitEvent<Record<string, any>>) => {
  if (!values.text) return
  await invoiceService.order.driverComment.create({text: values.text}, {}, {invoice_id: props.invoice.id, order_id: props.order.uuid})
  await refetch()
}

const updateComment = async (id: number, comment: DriverComment) => {
  await invoiceService.order.driverComment.update(id, {text: comment.text}, {}, {invoice_id: props.invoice.id, order_id: props.order.uuid})
  comment.status = 'loading'
}

onMounted(async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
})

defineEmits(['close'])
</script>

<template>
  <Loading :loading="isFetching">
    <div class="min-h-[300px] max-h-[600px] flex flex-col justify-between">
      <div ref="chatContainer" class="h-full w-full overflow-y-auto gap-3 flex flex-col mb-3">
        <div class="bg-surface-200 rounded-md p-2" v-for="comment in comments" :key="comment.id">
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
          {{ comments?.length }} комментариев
        </div>
      </div>
      <div v-if="!order.done">
        <Form method="post" @submit="send">
          <InputGroup class="border border-surface-200 rounded-md">
            <Button severity="secondary" @click="() => refetch()">
              <RefreshCcw />
            </Button>
            <InputText class="border-none" name="text" placeholder="Введите текст..." />
            <Button type="submit">
              <SendHorizonal />
            </Button>
          </InputGroup>
        </Form>
      </div>
    </div>
  </Loading>
</template>
