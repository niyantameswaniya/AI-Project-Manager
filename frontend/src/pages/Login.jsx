import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { employeeService } from '../services/api'

const Login = () => {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('manager')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    setError('')
    if (!email.trim() || !password.trim()) {
      setError('Please enter both email and password.')
      return
    }
    // Only validate employee logins against existing employees.
    if (role === 'employee') {
      setLoading(true)
      employeeService
        .getAll()
        .then((res) => {
          const employees = res.data || []
          const found = employees.some(
            (emp) => emp.email && emp.email.toLowerCase() === email.trim().toLowerCase()
          )
          if (!found) {
            setError('Invalid credentials.')
            setLoading(false)
            return
          }
          localStorage.setItem('role', role)
          navigate('/my-projects')
        })
        .catch(() => {
          setError('Unable to validate employee. Try again later.')
          setLoading(false)
        })
      return
    }

    // For manager, do not validate credentials (per instruction).
    localStorage.setItem('role', role)
    if (role === 'manager') navigate('/')
    else navigate('/my-projects')
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-luxury-noir">
      <div className="luxury-section w-full max-w-md p-8">
        <h2 className="text-2xl font-bold mb-4 text-luxury-white">Sign in</h2>
        <p className="text-sm text-luxury-wasabi/80 mb-6">Enter your credentials and select a role.</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-luxury-wasabi mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full luxury-input"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm text-luxury-wasabi mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full luxury-input"
              placeholder="••••••••"
            />
          </div>

          <div>
            <span className="block text-sm text-luxury-wasabi mb-2">Role</span>
            <div className="flex gap-4">
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="role"
                  value="manager"
                  checked={role === 'manager'}
                  onChange={() => setRole('manager')}
                />
                <span className="text-sm text-luxury-white">Manager</span>
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="radio"
                  name="role"
                  value="employee"
                  checked={role === 'employee'}
                  onChange={() => setRole('employee')}
                />
                <span className="text-sm text-luxury-white">Employee</span>
              </label>
            </div>
          </div>

          {error && <div className="text-red-400 text-sm">{error}</div>}

          <div className="flex flex-col gap-3">
            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-3 rounded-lg bg-luxury-earth text-white font-medium disabled:opacity-60"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
            <div className="text-center">
              <small className="text-xs text-luxury-wasabi/70">
                Tip: this demo doesn't check credentials — selecting a role will show the corresponding UI.
              </small>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}

export default Login

