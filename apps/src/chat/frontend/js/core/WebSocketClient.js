export default class WebSocketClient {
    constructor() {
        this.onOpen = null;
        this.onMessage = null;
        this.onClose = null;
        const protocol = location.protocol === "https:" ? "wss" : "ws";
        this.socket = new WebSocket(`${protocol}://${location.host}/`);
        this.socket.onopen = () => {
            this.onOpen?.();
        };
        this.socket.onmessage = (event) => {
            this.onMessage?.(event);
        };
        this.socket.onclose = (event) => {
            this.onClose?.(event);
        };
    }
    getSocket() {
        return this.socket;
    }
    sendData(data) {
        const serializedData = JSON.stringify(data);
        this.socket.send(serializedData);
    }
}
