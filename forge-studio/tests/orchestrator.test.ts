import { describe, it, expect, vi } from 'vitest';
import { EngineOrchestrator } from '../src/main/orchestrator';

describe('EngineOrchestrator', () => {
    it('should launch a process and capture output', async () => {
        const orchestrator = new EngineOrchestrator();
        const logSpy = vi.fn();
        
        orchestrator.onLog(logSpy);
        
        // Launch a simple echo command (mocking python -c "print('hello')")
        await orchestrator.launch('echo', ['hello-forge']);
        
        // Wait a bit for output
        await new Promise(resolve => setTimeout(resolve, 500));
        
        expect(logSpy).toHaveBeenCalledWith(expect.stringContaining('hello-forge'));
    });
});
