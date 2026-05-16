import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';
import { EngineOrchestrator } from './orchestrator';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow: BrowserWindow | null = null;
const orchestrator = new EngineOrchestrator();

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// Orchestrator IPC handlers
ipcMain.handle('launch-engine', async () => {
  try {
    // For now, we launch a simple echo or a python command if available
    // In a real scenario, this would be the game engine
    await orchestrator.launch('python3', ['src/main.py']);
    return { success: true };
  } catch (error: any) {
    return { success: false, error: error.message };
  }
});

orchestrator.onLog((data) => {
  mainWindow?.webContents.send('engine-log', data);
});
