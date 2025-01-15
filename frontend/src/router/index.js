import { createRouter, createWebHistory } from 'vue-router';
import others from './others'
import AppLayout from "@/layout/AppLayout.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'main',
                    component: () => import('@/views/Main.vue')
                },
                {
                    path: '/invite',
                    name: 'invite',
                    component: () => import('@/views/invites/Invites.vue')
                },
                {
                    path: '/car',
                    name: 'cars',
                    component: () => import('@/views/Cars.vue')
                },
                {
                    path: '/driver',
                    name: 'drivers',
                    component: () => import('@/views/Drivers.vue')
                },
            ],
        },
        ...others
    ]
});

export default router;
