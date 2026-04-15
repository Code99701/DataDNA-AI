import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import UploadPage from './features/upload/UploadPage';
import Dashboard from './pages/Dashboard';
import RegisterPage from './features/identity/RegisterPage';
import IdentifyPage from './features/identity/IdentifyPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/identify" element={<IdentifyPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
