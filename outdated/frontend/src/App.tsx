import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.scss'
import { Header } from './components';
import HomePage from './pages/HomePage'
import UserPage from './pages/UserPage'
import LoginPage from './pages/auth/LoginPage'
import RegisterPage from './pages/auth/RegisterPage'

function App() {

  return (
    <BrowserRouter>
      {/* 1. Header is OUTSIDE of Routes, so it never disappears or reloads */}
      <Header /> 

      <main className="content">
        {/* 2. The Switchboard decides which page to show */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/user/" element={<UserPage />} />
          <Route path="/login/" element={<LoginPage />} />
          <Route path="/register/" element={<RegisterPage />} />


          {/* 3. A "404" fallback for React */}
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

export default App
