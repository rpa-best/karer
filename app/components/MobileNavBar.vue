<template>
    <div
        class="z-[999] p-2 rounded-t-2xl w-full md:hidden h-[70px] bg-background fixed bottom-0 left-0 right-0 flex flex-row justify-around shadow-md">
        <a class="flex flex-col items-center" :href="p('/')" :class="useRoute().path === '/my' ? 'text-primary' : ''">
            <BookText />
            <p>{{ $t('Заявки') }}</p>
        </a>
        <a class="flex flex-col items-center" :href="p('/driver')"
            :class="useRoute().path === '/driver' ? 'text-primary' : ''">
            <Users />
            <p>{{ $t('Водители') }}</p>
        </a>
        <a class="flex flex-col items-center" :href="p('/car')"
            :class="useRoute().path === '/car' ? 'text-primary' : ''">
            <Truck />
            <p>{{ $t('Автомобили') }}</p>
        </a>

        <a class="flex flex-col items-center" @click="profile_open = true">
            <MenuIcon />
            <p>{{ $t('Профиль') }}</p>
        </a>
        <Drawer position="right" v-model:visible="profile_open" class="!w-[350px]">
            <template #header>
                <Logo />
            </template>
            <SidebarContent class="mb-3">
                <button v-if="user.id" v-ripple
                    class="relative overflow-hidden w-full border-0 bg-transparent flex items-center p-2 pl-4 hover:bg-surface-100 rounded-none cursor-pointer transition-colors duration-200">
                    <Avatar v-if="user.first_name" :label="user.first_name[0]" class="mr-2 cursor-pointer" shape="circle"
                        @click="toggle" size="large" />
                    <span class="inline-flex flex-col items-start">
                        <span class="font-bold">{{ user.first_name }} {{ user.last_name }}</span>
                    </span>
                </button>
                <h2 v-else class="font-bold text-lg">{{ $t('Пользователь') }}</h2>
            </SidebarContent>
            <AppSidebar class="!h-auto" />
            <Button v-if="user.id" class="w-full mt-2" severity="danger" @click="logout">
                {{ $t('Выйти') }}
            </Button>
        </Drawer>
    </div>
</template>
<script>
import { BookText, Users, Truck, Menu } from 'lucide-vue-next'
import { useUser } from "@/store/user"

export default {
    components: {BookText, Users, Truck, MenuIcon: Menu},
    data() {
        return {
            profile_open: false,
        }
    },
    computed: {
        user: () => useUser().user,
        path: () => useRoute().fullPath
    },
    watch: {
        path() {
            this.profile_open = false
        }
    },
    methods: {
        p: (value) => useLocalePath()(value),
        logout: () => useUser().logout()
    }
}
</script>