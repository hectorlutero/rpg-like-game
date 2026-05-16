import fs from 'fs/promises';
import path from 'path';

/**
 * SmartDataManager handles safe JSON persistence with field preservation.
 */
export class SmartDataManager {
    /**
     * Saves data to a JSON file. If the file already exists, it merges the new data
     * with the existing data, preserving any fields not present in the new data.
     * 
     * @param filePath - Path to the JSON file.
     * @param newData - Data to merge and save.
     */
    async smartSave(filePath: string, newData: any): Promise<void> {
        let finalData = newData;

        try {
            const content = await fs.readFile(filePath, 'utf-8');
            const existingData = JSON.parse(content);
            finalData = this.deepMerge(existingData, newData);
        } catch (error: any) {
            if (error.code !== 'ENOENT') {
                throw error;
            }
            // If file doesn't exist, we just use newData (handled by initialization)
        }

        const dir = path.dirname(filePath);
        await fs.mkdir(dir, { recursive: true });
        await fs.writeFile(filePath, JSON.stringify(finalData, null, 2), 'utf-8');
    }

    /**
     * Deeply merges two objects. 
     * Objects are merged recursively, arrays and primitives are replaced.
     */
    private deepMerge(target: any, source: any): any {
        if (!this.isObject(target) || !this.isObject(source)) {
            return source;
        }

        const output = { ...target };
        
        for (const key of Object.keys(source)) {
            if (this.isObject(source[key])) {
                if (!(key in target)) {
                    Object.assign(output, { [key]: source[key] });
                } else {
                    output[key] = this.deepMerge(target[key], source[key]);
                }
            } else {
                Object.assign(output, { [key]: source[key] });
            }
        }
        
        return output;
    }

    private isObject(item: any): boolean {
        return (item && typeof item === 'object' && !Array.isArray(item));
    }
}
