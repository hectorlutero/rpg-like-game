import { describe, it, expect, vi, beforeEach } from 'vitest';
import { VenvManager } from '../src/main/venv-manager';
import fs from 'fs/promises';
import { spawn } from 'child_process';
import path from 'path';

vi.mock('fs/promises');
vi.mock('child_process');

describe('VenvManager', () => {
    const projectRoot = '/mock/root';
    const venvPath = path.join(projectRoot, '.forge_venv');

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should detect existing venv', async () => {
        vi.mocked(fs.access).mockResolvedValue(undefined);
        const manager = new VenvManager(projectRoot);
        
        const exists = await manager.venvExists();
        expect(exists).toBe(true);
        expect(fs.access).toHaveBeenCalledWith(venvPath);
    });

    it('should create venv if it does not exist', async () => {
        vi.mocked(fs.access).mockRejectedValue(new Error('File not found'));
        
        const mockSpawn = vi.mocked(spawn);
        mockSpawn.mockReturnValue({
            on: vi.fn((event, cb) => {
                if (event === 'close') cb(0);
            }),
            stdout: { on: vi.fn() },
            stderr: { on: vi.fn() },
        } as any);

        const manager = new VenvManager(projectRoot);
        await manager.ensureVenv();

        // Check if python -m venv was called
        expect(mockSpawn).toHaveBeenCalledWith('python3', ['-m', 'venv', venvPath]);
    });

    it('should install requirements', async () => {
        vi.mocked(fs.access).mockResolvedValue(undefined); // Venv exists
        
        const mockSpawn = vi.mocked(spawn);
        mockSpawn.mockReturnValue({
            on: vi.fn((event, cb) => {
                if (event === 'close') cb(0);
            }),
            stdout: { on: vi.fn() },
            stderr: { on: vi.fn() },
        } as any);

        const manager = new VenvManager(projectRoot);
        await manager.installRequirements();

        const pipPath = path.join(venvPath, process.platform === 'win32' ? 'Scripts' : 'bin', 'pip');
        const reqPath = path.join(projectRoot, 'requirements.txt');
        
        expect(mockSpawn).toHaveBeenCalledWith(pipPath, ['install', '-r', reqPath]);
    });
});
