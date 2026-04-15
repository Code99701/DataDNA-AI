import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import UploadPage    from './features/upload/UploadPage';
import VerifyPage    from './features/verify/VerifyPage';
import RegisterPage  from './features/identity/RegisterPage';
import IdentifyPage  from './features/identity/IdentifyPage';
import Dashboard     from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="app-wrapper">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/"          element={<UploadPage />}   />
            <Route path="/verify"    element={<VerifyPage />}   />
            <Route path="/register"  element={<RegisterPage />} />
            <Route path="/identify"  element={<IdentifyPage />} />
            <Route path="/dashboard" element={<Dashboard />}    />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;