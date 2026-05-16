import { WebSocketServer, WebSocket } from 'ws';
import { EventEmitter } from 'events';

export class SocketManager extends EventEmitter {
    private wss: WebSocketServer | null = null;
    private clients: Set<WebSocket> = new Set();
    private port: number = 8080;

    constructor(port: number = 8080) {
        super();
        this.port = port;
    }

    start() {
        this.wss = new WebSocketServer({ port: this.port });
        
        this.wss.on('connection', (ws: WebSocket) => {
            console.log('New engine connection');
            this.clients.add(ws);

            ws.on('message', (data: string) => {
                try {
                    const message = JSON.parse(data.toString());
                    if (message.type === 'HANDSHAKE') {
                        ws.send(JSON.stringify({ type: 'HANDSHAKE_ACK', status: 'connected' }));
                        this.emit('connected');
                    }
                    this.emit('message', message);
                } catch (e) {
                    console.error('Failed to parse message:', data);
                }
            });

            ws.on('close', () => {
                this.clients.delete(ws);
                this.emit('disconnected');
            });

            ws.on('error', (err) => {
                console.error('WebSocket error:', err);
            });
        });

        console.log(`WebSocket server started on port ${this.port}`);
    }

    broadcast(message: any) {
        const data = JSON.stringify(message);
        this.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(data);
            }
        });
    }

    stop() {
        if (this.wss) {
            this.wss.close();
            this.wss = null;
        }
    }
}
