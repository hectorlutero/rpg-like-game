import { useState, useEffect, useRef } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

interface ElectronAPI {
  launchEngine: () => Promise<{ success: boolean; error?: string }>;
  onEngineLog: (callback: (data: string) => void) => () => void;
  onEngineConnectionStatus: (callback: (status: string) => void) => () => void;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}

function App() {
  const [count, setCount] = useState(0)
  const [logs, setLogs] = useState<string[]>([])
  const [connectionStatus, setConnectionStatus] = useState<string>('disconnected')
  const terminalEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const removeLogListener = window.electronAPI.onEngineLog((data) => {
      setLogs((prev) => [...prev, data])
    })
    
    const removeStatusListener = window.electronAPI.onEngineConnectionStatus((status) => {
      setConnectionStatus(status)
    })

    return () => {
      removeLogListener()
      removeStatusListener()
    }
  }, [])

  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  const handleLaunch = async () => {
    setLogs((prev) => [...prev, '> Launching engine...'])
    const result = await window.electronAPI.launchEngine()
    if (!result.success) {
      setLogs((prev) => [...prev, `Error: ${result.error}`])
    }
  }

  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Forge Studio</h1>
          <p>
            Control Center for The Forge Engine | Status: <span style={{ color: connectionStatus === 'connected' ? '#4CAF50' : '#f44336' }}>{connectionStatus.toUpperCase()}</span>
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            type="button"
            className="counter"
            onClick={() => setCount((count) => count + 1)}
          >
            Count is {count}
          </button>
          
          <button
            type="button"
            className="launch-button"
            onClick={handleLaunch}
          >
            Launch Engine
          </button>
        </div>

        <div className="terminal">
          {logs.map((log, i) => (
            <p key={i} className="terminal-line">{log}</p>
          ))}
          <div ref={terminalEndRef} />
        </div>
      </section>

      <div className="ticks"></div>

      <section id="next-steps">
        <div id="docs">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#documentation-icon"></use>
          </svg>
          <h2>Documentation</h2>
          <p>Your questions, answered</p>
          <ul>
            <li>
              <a href="https://vite.dev/" target="_blank">
                <img className="logo" src={viteLogo} alt="" />
                Explore Vite
              </a>
            </li>
            <li>
              <a href="https://react.dev/" target="_blank">
                <img className="button-icon" src={reactLogo} alt="" />
                Learn more
              </a>
            </li>
          </ul>
        </div>
        <div id="social">
          <svg className="icon" role="presentation" aria-hidden="true">
            <use href="/icons.svg#social-icon"></use>
          </svg>
          <h2>Connect with us</h2>
          <p>Join the Vite community</p>
          <ul>
            <li>
              <a href="https://github.com/vitejs/vite" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#github-icon"></use>
                </svg>
                GitHub
              </a>
            </li>
            <li>
              <a href="https://chat.vite.dev/" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#discord-icon"></use>
                </svg>
                Discord
              </a>
            </li>
            <li>
              <a href="https://x.com/vite_js" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#x-icon"></use>
                </svg>
                X.com
              </a>
            </li>
            <li>
              <a href="https://bsky.app/profile/vite.dev" target="_blank">
                <svg
                  className="button-icon"
                  role="presentation"
                  aria-hidden="true"
                >
                  <use href="/icons.svg#bluesky-icon"></use>
                </svg>
                Bluesky
              </a>
            </li>
          </ul>
        </div>
      </section>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default App
