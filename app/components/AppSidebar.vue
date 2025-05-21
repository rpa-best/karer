<template>
    <div class="flex flex-col justify-between h-[98vh] gap-4">
      <SidebarContent class="h-full">
        <Logo class="justify-center mb-3 hidden md:flex" />

        <Menu :model="sidebar()" class="p-0 !bg-transparent !border-0">
          <template #item="{ item }">
            <NuxtLink :class="route.path === item.url ? 'text-primary' : ''" :to="item.url" class="flex flex-row px-3 py-2 cursor-pointer">
              <component v-if="item.icon" :is="item.icon" />
                <span class="ml-2">{{ $t(item.title) }}</span>
                <Badge severity="danger" class="ml-2" v-if="item.disabled" :value="$t('Скоро')"/>
            </NuxtLink>
          </template>
        </Menu>
      </SidebarContent>
      <SidebarContent class="md:flex hidden items-center">
        <UserDropdown />
        <Notifications />
      </SidebarContent>
    </div>
</template>
<script setup lang="ts">
import sidebar from '@/layouts/sidebar-config'
import SidebarContent from './SidebarContent.vue';
import UserDropdown from './UserDropdown.vue';
import { useRoute } from 'vue-router';

const route = useRoute()
</script>