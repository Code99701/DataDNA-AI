import React from 'react';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Application</h1>
        <nav>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
          </ul>
        </nav>
      </header>
      <main>
        {/* Placeholder for basic routing logic or you can integrate react-router */}
        <Home />
        <hr />
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
