import { spawn, ChildProcess } from 'child_process';

export class EngineOrchestrator {
    private process: ChildProcess | null = null;
    private logCallbacks: ((data: string) => void)[] = [];

    onLog(callback: (data: string) => void) {
        this.logCallbacks.push(callback);
    }

    async launch(command: string, args: string[]): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                this.process = spawn(command, args);

                this.process.stdout?.on('data', (data) => {
                    const str = data.toString();
                    this.logCallbacks.forEach(cb => cb(str));
                });

                this.process.stderr?.on('data', (data) => {
                    const str = data.toString();
                    this.logCallbacks.forEach(cb => cb(`ERROR: ${str}`));
                });

                this.process.on('error', (err) => {
                    this.logCallbacks.forEach(cb => cb(`SPAWN ERROR: ${err.message}`));
                    reject(err);
                });

                // In a real scenario, we might wait for a specific signal or just success
                resolve();
            } catch (err) {
                reject(err);
            }
        });
    }

    stop() {
        if (this.process) {
            this.process.kill();
            this.process = null;
        }
    }
}
