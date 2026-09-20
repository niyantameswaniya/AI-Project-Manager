import axios from 'axios'

// Use same origin when served from backend (port 8000), else dev server (8000)
const API_BASE_URL = import.meta.env.DEV ? 'http://localhost:8000' : ''

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const projectService = {
  getAll: () => api.get('/api/projects'),
  getById: (id) => api.get(`/api/projects/${id}`),
  create: (data) => api.post('/api/projects', data),
  predict: (id) => api.post(`/api/projects/${id}/predict`),
  assign: (projectId, employeeIds) =>
    api.post(`/api/projects/${projectId}/assign`, { employee_ids: employeeIds }),
}

export const employeeService = {
  getAll: () => api.get('/api/employees'),
  getById: (id) => api.get(`/api/employees/${id}`),
  getProjects: (employeeId) => api.get(`/api/employees/${employeeId}/projects`),
  create: (data) => api.post('/api/employees', data),
}

export const analyticsService = {
  getAnalytics: () => api.get('/api/analytics'),
}

export default api


