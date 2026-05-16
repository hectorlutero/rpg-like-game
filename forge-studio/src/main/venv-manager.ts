import fs from 'fs/promises';
import { spawn } from 'child_process';
import path from 'path';

export class VenvManager {
    private venvPath: string;
    private projectRoot: string;

    constructor(projectRoot: string) {
        this.projectRoot = projectRoot;
        this.venvPath = path.join(projectRoot, '.forge_venv');
    }

    async venvExists(): Promise<boolean> {
        try {
            await fs.access(this.venvPath);
            return true;
        } catch {
            return false;
        }
    }

    async ensureVenv(): Promise<void> {
        if (!(await this.venvExists())) {
            console.log('Creating virtual environment...');
            await this.runCommand('python3', ['-m', 'venv', this.venvPath]);
            await this.installRequirements();
        }
    }

    async installRequirements(): Promise<void> {
        const pipPath = this.getPipExecutable();
        const requirementsPath = path.join(this.projectRoot, 'requirements.txt');
        console.log('Installing requirements...');
        await this.runCommand(pipPath, ['install', '-r', requirementsPath]);
    }

    getPythonExecutable(): string {
        const binDir = process.platform === 'win32' ? 'Scripts' : 'bin';
        const execName = process.platform === 'win32' ? 'python.exe' : 'python3';
        return path.join(this.venvPath, binDir, execName);
    }

    private getPipExecutable(): string {
        const binDir = process.platform === 'win32' ? 'Scripts' : 'bin';
        const execName = process.platform === 'win32' ? 'pip.exe' : 'pip';
        return path.join(this.venvPath, binDir, execName);
    }

    private runCommand(command: string, args: string[]): Promise<void> {
        return new Promise((resolve, reject) => {
            const process = spawn(command, args);

            process.on('close', (code) => {
                if (code === 0) {
                    resolve();
                } else {
                    reject(new Error(`Command ${command} failed with code ${code}`));
                }
            });

            process.on('error', (err) => {
                reject(err);
            });
        });
    }
}
