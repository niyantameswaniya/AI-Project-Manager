import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, Upload, BarChart3, Users, Sparkles, Briefcase } from 'lucide-react'
import { motion } from 'framer-motion'

const Navbar = () => {
  const location = useLocation()

  const managerItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/upload', label: 'Upload Project', icon: Upload },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/employees', label: 'Employees', icon: Users },
  ]

  const employeeItems = [{ path: '/my-projects', label: 'My Projects', icon: Briefcase }]

  // read role from localStorage; possible values: 'manager' | 'employee' | null
  const role = typeof window !== 'undefined' ? localStorage.getItem('role') : null

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="luxury-section mx-4 mt-4 mb-8 px-6 py-4"
    >
      <div className="flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="bg-luxury-earth p-2 rounded-lg">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <span className="font-display text-2xl font-bold text-luxury-white group-hover:text-luxury-earth transition-colors">
            AI Project Manager
          </span>
        </Link>

        <div className="flex items-center gap-2">
          {role === 'manager' && (
            <>
              <span className="text-xs text-luxury-wasabi/80 mr-2 hidden md:inline">Manager</span>
              {managerItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                      isActive
                        ? 'bg-luxury-earth/30 text-luxury-white border border-luxury-earth/50'
                        : 'text-luxury-wasabi hover:bg-luxury-emerald/30 hover:text-luxury-white'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                )
              })}
            </>
          )}

          {role === 'employee' && (
            <>
              <span className="text-xs text-luxury-wasabi/80 mr-2 hidden md:inline">Employee</span>
              {employeeItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                      isActive
                        ? 'bg-luxury-wasabi/30 text-luxury-white border border-luxury-wasabi/50'
                        : 'text-luxury-wasabi hover:bg-luxury-emerald/30 hover:text-luxury-white'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                )
              })}
            </>
          )}

          {!role && (
            <Link
              to="/login"
              className="px-4 py-2 rounded-lg text-luxury-wasabi hover:bg-luxury-emerald/30 hover:text-luxury-white"
            >
              Sign in
            </Link>
          )}

          {role && (
            <button
              onClick={() => {
                localStorage.removeItem('role')
                // reload to reflect menu change
                window.location.href = '/login'
              }}
              className="ml-2 px-3 py-2 rounded-lg bg-transparent text-sm text-luxury-wasabi hover:bg-luxury-emerald/20"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </motion.nav>
  )
}

export default Navbar
