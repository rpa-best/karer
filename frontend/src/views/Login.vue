<script>
import FloatingConfigurator from '@/components/FloatingConfigurator.vue';
import {Form} from '@primevue/forms';
import {useUser} from "@/store";

export default {
    name: 'Login',
    components: {FloatingConfigurator, Form},
    data() {
        return {
            authed: false,
            email: null,
            password: null,
            career: null,
        }
    },
    methods: {
        auth(e) {
            if (e.valid) {
                this.authed = true
                useUser().auth(e.states.email.value, e.states.password.value)
            }
        },
        resolver_auth({values}) {
            const errors = {};
            if (!values.email) {
                errors.email = [{message: 'Электронная почта обязательное поле.'}];
            }

            if (!values.password) {
                errors.password = [{message: 'Пароль обязательное поле.'}];
            }
            return {
                errors
            };
        },
        login(e) {
            if (e.valid) {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Авторизация прошла успешно',
                    life: 3000
                });
                useUser().set_career(e.states.career.value)
                this.$router.push(this.$route.query.next ?? "/")
            }
        },
        resolver_login({values}) {
            const errors = {};
            if (!values.career) {
                errors.career = [{message: 'Карьер обязательное поле.'}];
            }
            return {
                errors
            };
        },
    },
    computed: {
        careers: () => useUser().careers
    }
}
</script>

<template>
    <div class="flex">
        <div class="w-full md:w-5">
            <FloatingConfigurator/>
            <div
                class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen overflow-hidden">
                <div class="flex flex-row items-center justify-center w-full"
                     style="max-width: 500px; position: relative; height: 600px; overflow: hidden">

                    <div class="py-20 px-8 sm:px-20 w-full" :class="{'login-authed': authed}"
                         style="position: absolute; left: 0; transition: 1s">
                        <h2 style="font-size: 26px; font-weight: bold" class="mb-3">Вход</h2>
                        <Form v-slot="$form" @submit="auth" :resolver="resolver_auth">
                            <div>
                                <label for="email"
                                       class="block text-surface-900 dark:text-surface-0 text-l font-medium mb-2">Почта</label>
                                <InputText id="email" type="email" placeholder="Введите почту" name="email"
                                           class="w-full md:w-[30rem] mb-2"/>
                                <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple" class="mb-3">
                                    {{ $form.email.error?.message }}
                                </Message>
                                <label for="password"
                                       class="block text-surface-900 dark:text-surface-0 font-medium text-l mb-2">Пароль</label>
                                <Password id="password" placeholder="Введите пароль"
                                          :toggleMask="true" name="password"
                                          class="mb-2" fluid :feedback="false"></Password>
                                <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple" class="mb-3">
                                    {{ $form.password.error?.message }}
                                </Message>
                                <div class="flex items-center justify-between mt-2 mb-4 gap-8">
                                    <span class="font-medium no-underline ml-2 text-right cursor-pointer text-primary">Забыли пароль?</span>
                                </div>
                                <Button type="submit" label="Продолжить" class="w-full"></Button>
                            </div>
                        </Form>
                    </div>

                    <div class="py-20 px-8 sm:px-20 w-full" :class="{'career-authed': authed}"
                         style="position: absolute;left: 100%; transition: 1s">
                        <div class="mb-3">
                            <button type="button" @click="authed = false">
                                <i class="pi pi-arrow-left" style="font-size: 20px"></i>
                            </button>
                        </div>
                        <h2 style="font-size: 26px; font-weight: bold" class="mb-3">Здравствуйте, Иван! Выберите
                            карьер</h2>
                        <Form v-slot="$form" @submit="login" :resolver="resolver_login">
                        <div>
                            <Select name="career" :options="careers" optionLabel="name" option-value="id"
                                    placeholder="Выберите карьер" class="w-full mb-3"/>
                            <Message v-if="$form.career?.invalid" severity="error" size="small" variant="simple" class="mb-3">
                                {{ $form.career.error?.message }}
                            </Message>
                            <Button type="submit" label="Продолжить" class="w-full"></Button>
                        </div>
                            </Form>
                    </div>
                </div>
            </div>
        </div>
        <div class="w-0 md:w-7 flex align-items-center justify-content-center bg-surface-50 dark:bg-surface-950">
            <div
                style="background-image: url('/login.svg'); background-size: cover; width: 80%; height: 80%; border-radius: 40px"></div>
        </div>
    </div>

</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}

.login-authed {
    transition: 1s;
    left: -100% !important;
}

.career-authed {
    transition: 1s;
    left: 0 !important;
}
</style>
