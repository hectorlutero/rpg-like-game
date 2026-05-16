import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  launchEngine: () => ipcRenderer.invoke('launch-engine'),
  smartSave: (filePath: string, data: any) => ipcRenderer.invoke('smart-save', { filePath, data }),
  onEngineLog: (callback: (data: string) => void) => {
    const subscription = (_event: any, data: string) => callback(data);
    ipcRenderer.on('engine-log', subscription);
    return () => ipcRenderer.removeListener('engine-log', subscription);
  },
  onEngineConnectionStatus: (callback: (status: string) => void) => {
    const subscription = (_event: any, status: string) => callback(status);
    ipcRenderer.on('engine-connection-status', subscription);
    return () => ipcRenderer.removeListener('engine-connection-status', subscription);
  },
});
