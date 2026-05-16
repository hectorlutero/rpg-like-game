import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { SmartDataManager } from '../src/main/data-manager';
import fs from 'fs/promises';
import path from 'path';
import os from 'os';

describe('SmartDataManager', () => {
    let tempDir: string;
    let testFilePath: string;
    let dataManager: SmartDataManager;

    beforeEach(async () => {
        tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'forge-test-'));
        testFilePath = path.join(tempDir, 'test.json');
        dataManager = new SmartDataManager();
    });

    afterEach(async () => {
        await fs.rm(tempDir, { recursive: true, force: true });
    });

    it('should create a new file if it does not exist', async () => {
        const data = { name: 'New Item', value: 10 };
        await dataManager.smartSave(testFilePath, data);
        
        const content = await fs.readFile(testFilePath, 'utf-8');
        expect(JSON.parse(content)).toEqual(data);
    });

    it('should merge new data with existing data, preserving unknown fields', async () => {
        const existingData = { 
            id: 'item-1',
            metadata: { 
                creator: 'admin',
                tags: ['alpha']
            },
            stats: {
                hp: 100,
                mp: 50
            }
        };
        await fs.writeFile(testFilePath, JSON.stringify(existingData, null, 2));

        const newData = {
            stats: {
                hp: 120 // Update HP
            },
            metadata: {
                tags: ['beta'] // Replace tags
            }
        };

        await dataManager.smartSave(testFilePath, newData);

        const content = await fs.readFile(testFilePath, 'utf-8');
        const savedData = JSON.parse(content);

        // Check preserved fields
        expect(savedData.id).toBe('item-1');
        expect(savedData.metadata.creator).toBe('admin');
        expect(savedData.stats.mp).toBe(50);

        // Check updated fields
        expect(savedData.stats.hp).toBe(120);
        expect(savedData.metadata.tags).toEqual(['beta']);
    });
});
