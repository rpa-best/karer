<script setup lang="ts">
import { Pen, Plus, ChevronDown } from "lucide-vue-next"
import type { Driver, Sender } from "~/types/onec"
import { DriverService, SenderService } from '~/services'
import { useQuery } from '@tanstack/vue-query'

const driver = ref<Driver | null>(null)
const show_driver = ref(false)
const driverService = new DriverService()
const senderService = new SenderService()

const searchQuery = ref('')

const { data: senders } = useQuery({
  queryKey: ['senders'],
  queryFn: async () => await senderService.list<Sender[]>()
})

const expandedSenders = reactive<Record<number, boolean>>({})
const driversBySender = reactive<Record<number, Driver[]>>({})
const fetchingSender = reactive<Record<number, boolean>>({})

async function fetchSenderDrivers(senderId: number) {
  fetchingSender[senderId] = true
  try {
    driversBySender[senderId] = await driverService.list<Driver[]>({
      sender: senderId,
      search: searchQuery.value || undefined
    })
  } finally {
    fetchingSender[senderId] = false
  }
}

function toggleSection(senderId: number) {
  expandedSenders[senderId] = !expandedSenders[senderId]
  if (expandedSenders[senderId] && !driversBySender[senderId]) {
    fetchSenderDrivers(senderId)
  }
}

async function onSearch() {
  for (const [id, expanded] of Object.entries(expandedSenders)) {
    if (expanded) await fetchSenderDrivers(Number(id))
  }
}

async function onDriverClose(flag: boolean) {
  driver.value = null
  show_driver.value = false
  if (flag) {
    for (const [id, expanded] of Object.entries(expandedSenders)) {
      if (expanded) await fetchSenderDrivers(Number(id))
    }
  }
}

const rowClick = (data: Driver | null = null) => {
  show_driver.value = true
  driver.value = data
}

// JS-хуки для плавной анимации высоты
function beforeEnter(el: Element) {
  const e = el as HTMLElement
  e.style.height = '0'
  e.style.opacity = '0'
  e.style.overflow = 'hidden'
}
function enter(el: Element, done: () => void) {
  const e = el as HTMLElement
  requestAnimationFrame(() => {
    e.style.transition = 'height 0.35s ease, opacity 0.3s ease'
    e.style.height = e.scrollHeight + 'px'
    e.style.opacity = '1'
    e.addEventListener('transitionend', () => {
      e.style.height = 'auto'
      e.style.overflow = ''
      done()
    }, { once: true })
  })
}
function beforeLeave(el: Element) {
  const e = el as HTMLElement
  e.style.height = e.scrollHeight + 'px'
  e.style.overflow = 'hidden'
}
function leave(el: Element, done: () => void) {
  const e = el as HTMLElement
  requestAnimationFrame(() => {
    e.style.transition = 'height 0.3s ease, opacity 0.25s ease'
    e.style.height = '0'
    e.style.opacity = '0'
    e.addEventListener('transitionend', done, { once: true })
  })
}
</script>

<template>
  <div>
    <div class="flex justify-between items-center flex-wrap mb-6">
      <h2 class="text-3xl font-bold">Водители</h2>
      <div class="flex gap-3 md:flex-nowrap flex-wrap md:w-auto w-full mt-2">
        <IconField class="w-full">
          <InputText placeholder="Поиск" v-model="searchQuery" @keydown.enter="onSearch" class="w-full"/>
          <InputIcon>
            <i class="pi pi-search cursor-pointer" @click="onSearch"/>
          </InputIcon>
        </IconField>
        <Button class="mb-3 w-full" @click="() => rowClick()">
          <Plus/>
          Добавить водителя
        </Button>
      </div>
    </div>

    <div class="flex flex-col gap-4">
      <div v-for="sender in senders" :key="sender.id">
        <div
          @click="toggleSection(sender.id)"
          class="flex items-center justify-between px-5 py-4 rounded-xl cursor-pointer select-none text-white shadow-lg"
          style="background: linear-gradient(135deg, #00d8a5 0%, #8cd66a 100%)"
        >
          <div class="flex items-center gap-3">
            <span class="text-lg font-bold tracking-wide">{{ sender.name }}</span>
            <span
              v-if="driversBySender[sender.id]"
              class="text-sm font-semibold px-2.5 py-0.5 rounded-full"
              style="background: rgba(255,255,255,0.25)"
            >
              {{ driversBySender[sender.id].length }}
            </span>
          </div>
          <div class="flex items-center gap-2">
            <i v-if="fetchingSender[sender.id]" class="pi pi-spin pi-spinner text-white/80 text-sm"></i>
            <ChevronDown
              :size="20"
              class="transition-transform duration-300 ease-in-out"
              :style="{ transform: expandedSenders[sender.id] ? 'rotate(180deg)' : 'rotate(0deg)' }"
            />
          </div>
        </div>

        <Transition
          :css="false"
          @before-enter="beforeEnter"
          @enter="enter"
          @before-leave="beforeLeave"
          @leave="leave"
        >
          <div v-if="expandedSenders[sender.id]" class="mt-2">
            <Card>
              <template #content>
                <DataTable
                  size="large"
                  :value="driversBySender[sender.id]"
                  :loading="fetchingSender[sender.id]"
                  rowHover
                >
                  <Column field="inn" header="ИНН" style="font-weight: 600"></Column>
                  <Column field="name" header="ФИО" style="font-weight: 600"></Column>
                  <Column field="phone_number" header="Телефон" style="font-weight: 600"></Column>
                  <Column>
                    <template #body="{data}">
                      <Button @click.stop="rowClick(data)" severity="help" rounded class="size-8 !p-2">
                        <Pen/>
                      </Button>
                    </template>
                  </Column>
                  <template #empty>
                    <p class="text-center">Водители не найдены.</p>
                  </template>
                </DataTable>
              </template>
            </Card>
          </div>
        </Transition>
      </div>
    </div>
  </div>

  <Dialog v-model:visible="show_driver" @close="driver=null" modal header="Изменить водителя"
          :style="{ 'max-width': '500px', width: '100%'}">
    <Driver v-if="show_driver" :driver="driver" @close="onDriverClose"/>
  </Dialog>
</template>
