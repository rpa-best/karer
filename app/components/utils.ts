import {token} from "~/composables";

export class Client {
    url!: URL
    socket!: WebSocket

    constructor(url: string) {

        const { public: { NUXT_APP_BACKEND_HOST } } = useRuntimeConfig();
        const backend = new URL(NUXT_APP_BACKEND_HOST)
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'

        this.url = new URL([protocol, `//`, backend.host, backend.pathname, url].join(''))
        this.url.searchParams.set("token", token.value?.access ?? '')
    }

    onerror(e: Event) {
        console.log(`Websocket error: ${this.url}`);
    }

    onopen(e: Event) {
        console.log(`Websocket open: ${this.url}`);
    }

    onmessage(e: MessageEvent) {
        console.log(`Websocket message: ${this.url}`);
    }

    onclose(e: CloseEvent) {
        console.log(`Websocket close: ${this.url}`);
    }

    async send(data: any) {
        this.socket.send(JSON.stringify(data))
    }

    close() {
        this.socket.close()
    }

    connect() {
        try {
            this.socket = new WebSocket(this.url);
            this.socket.onopen = this.onopen
            this.socket.onmessage = this.onmessage
            this.socket.onclose = this.onclose
            this.socket.onerror = this.onerror
        } catch (e) {
            console.error(`Websocket connection failed: ${this.url}`);
        }
    }
}