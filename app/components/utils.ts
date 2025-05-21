import {token} from "~/composables";

export class Client {
    url!: URL
    socket!: WebSocket

    constructor(url: string,
                onopen: ((this: WebSocket, ev: Event) => any) | null,
                onmessage: ((this: WebSocket, ev: MessageEvent) => any) | null,
                onclose: ((this: WebSocket, ev: CloseEvent) => any) | null) {

        const { public: { NUXT_APP_BACKEND_HOST } } = useRuntimeConfig();
        const backend = new URL(NUXT_APP_BACKEND_HOST)
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'

        this.url = new URL([protocol, `//`, backend.host, backend.pathname, url].join(''))
        console.log(this.url)
        this.url.searchParams.set("token", token.value?.access ?? '')
        this.socket = new WebSocket(this.url);
        this.socket.onopen = onopen
        this.socket.onmessage = onmessage
        this.socket.onclose = onclose
        this.socket.onerror = this.onerror
    }

    onerror(e: Event) {
        console.log(e);
    }

    async send(data: any) {
        this.socket.send(JSON.stringify(data))
    }

    close() {
        this.socket.close()
    }
}