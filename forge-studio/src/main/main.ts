import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';
import { EngineOrchestrator } from './orchestrator';
import { VenvManager } from './venv-manager';
import { SocketManager } from './socket-manager';
import { SmartDataManager } from './data-manager';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.join(__dirname, '../../../');

let mainWindow: BrowserWindow | null = null;
const orchestrator = new EngineOrchestrator();
const venvManager = new VenvManager(projectRoot);
const socketManager = new SocketManager();
const dataManager = new SmartDataManager();

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

app.whenReady().then(async () => {
  // Start WebSocket server
  socketManager.start();

  // Ensure venv is ready on startup
  try {
    await venvManager.ensureVenv();
  } catch (error) {
    console.error('Failed to initialize virtual environment:', error);
  }
  
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
    await venvManager.ensureVenv();
    const pythonPath = venvManager.getPythonExecutable();
    const mainScript = path.join(projectRoot, 'src/main.py');
    
    await orchestrator.launch(pythonPath, [mainScript]);
    return { success: true };
  } catch (error: any) {
    return { success: false, error: error.message };
  }
});

// Data persistence IPC handlers
ipcMain.handle('smart-save', async (_event, { filePath, data }) => {
  try {
    // Resolve path relative to project root if it's not absolute
    const absolutePath = path.isAbsolute(filePath) 
      ? filePath 
      : path.join(projectRoot, filePath);
      
    await dataManager.smartSave(absolutePath, data);
    return { success: true };
  } catch (error: any) {
    console.error('Smart save failed:', error);
    return { success: false, error: error.message };
  }
});

orchestrator.onLog((data) => {
  mainWindow?.webContents.send('engine-log', data);
});

socketManager.on('connected', () => {
  mainWindow?.webContents.send('engine-connection-status', 'connected');
});

socketManager.on('disconnected', () => {
  mainWindow?.webContents.send('engine-connection-status', 'disconnected');
});
