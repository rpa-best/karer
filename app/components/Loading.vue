<template>
    <div v-if="loading" class="w-full h-full min-h-[200px] flex flex-col justify-center items-center">
        <slot name="label" />
        <div class="relative">
            <div class="top">
                <div class="square">
                    <div class="square">
                        <div class="square">
                            <div class="square">
                                <div class="square">
                                    <div class="square">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bottom">
                <div class="square">
                    <div class="square">
                        <div class="square">
                            <div class="square">
                                <div class="square">
                                    <div class="square">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="left">
                <div class="square">
                    <div class="square">
                        <div class="square">
                            <div class="square">
                                <div class="square">
                                    <div class="square">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="right">
                <div class="square">
                    <div class="square">
                        <div class="square">
                            <div class="square">
                                <div class="square">
                                    <div class="square">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <slot v-else />
</template>
<script setup lang="ts">
defineProps<{
    loading: boolean
}>()
</script>

<style scoped>
/* From Uiverse.io by NlghtM4re */
.square {
    width: 4px;
    height: 15px;
    background: var(--p-primary-color);
    border-radius: 10px;
    display: block;
    /*margin:10px;*/
    -webkit-animation: turn 2.5s ease infinite;
    animation: turn 2.5s ease infinite;
    box-shadow: var(--p-primary-color) 0px 1px 15px 0px;
}

.top {
    position: absolute;
    left: 40%;
    top: 50%;
    -webkit-transform: rotate(90deg);
    transform: rotate(90deg);
}

.bottom {
    position: absolute;
    left: 40%;
    top: 50%;
    -webkit-transform: rotate(-90deg);
    transform: rotate(-90deg);
}

.left {
    position: absolute;
    left: 40%;
    top: 50%;
}

.right {
    position: absolute;
    left: 40%;
    top: 50%;
    -webkit-transform: rotate(-180deg);
    transform: rotate(-180deg);
}

@-webkit-keyframes turn {
    0% {
        transform: translateX(0) translateY(0) rotate(0);
    }

    50% {
        transform: translateX(400%) translateY(100%) rotate(90deg);
    }

    100% {
        transform: translateX(0) translateY(0) rotate(0);
    }
}

@keyframes turn {
    0% {
        transform: translateX(0) translateY(0) rotate(0);
    }

    70% {
        transform: translateX(400%) translateY(100%) rotate(90deg);
    }

    100% {
        transform: translateX(0) translateY(0) rotate(0);
    }
}
</style>
