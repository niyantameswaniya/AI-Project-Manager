import React from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ProjectUpload from './pages/ProjectUpload'
import ProjectDetails from './pages/ProjectDetails'
import Analytics from './pages/Analytics'
import Employees from './pages/Employees'
import EmployeeUpload from './pages/EmployeeUpload'
import MyProjects from './pages/MyProjects'

function App() {
  // RouteGuard handles first-load routing:
  // - if no role in localStorage, redirect to /login
  // - if role exists and user is at /login, redirect to appropriate landing
  function RouteGuard() {
    const location = useLocation()
    const navigate = useNavigate()
    React.useEffect(() => {
      const role = typeof window !== 'undefined' ? localStorage.getItem('role') : null
      if (!role && location.pathname !== '/login') {
        navigate('/login')
      } else if (role && location.pathname === '/login') {
        if (role === 'manager') navigate('/')
        else navigate('/my-projects')
      }
    }, [location.pathname, navigate])
    return null
  }

  return (
    <Router>
      <div className="min-h-screen bg-luxury-noir">
        <RouteGuard />
        <Navbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<ProjectUpload />} />
          <Route path="/project/:id" element={<ProjectDetails />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/employees" element={<Employees />} />
          <Route path="/employees/upload" element={<EmployeeUpload />} />
          <Route path="/my-projects" element={<MyProjects />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

