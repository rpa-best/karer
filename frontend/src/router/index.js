import { createRouter, createWebHistory } from 'vue-router';
import others from './others'
import AppLayout from "@/layout/AppLayout.vue";
import {auth} from "@/middlewares"
import {isLogist} from "@/permissions";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            meta: {
                middleware: [auth]
            },
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
                    component: () => import('@/views/Cars.vue'),
                    meta: {
                        permissions: [isLogist]
                    },
                },
                {
                    path: '/driver',
                    name: 'drivers',
                    component: () => import('@/views/Drivers.vue'),
                    meta: {
                        permissions: [isLogist]
                    },
                },
            ],
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/views/Login.vue')
        },
        {
            path: '/auth/access',
            name: 'access',
            component: () => import('@/views/Access.vue')
        },
        ...others
    ]
});

router.beforeEach(async (to, from, next) => {
    if (to.meta && to.meta.middleware) {
        for (let func of to.meta.middleware) {
            await func({to, from, next})
        }
    }
    next()
})

export default router;
