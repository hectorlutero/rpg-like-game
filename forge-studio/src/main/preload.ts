import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  launchEngine: () => ipcRenderer.invoke('launch-engine'),
  onEngineLog: (callback: (data: string) => void) => {
    const subscription = (_event: any, data: string) => callback(data);
    ipcRenderer.on('engine-log', subscription);
    return () => ipcRenderer.removeListener('engine-log', subscription);
  },
});
