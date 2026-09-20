import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Briefcase, User, ChevronDown } from 'lucide-react'
import { employeeService } from '../services/api'

const MyProjects = () => {
  const [employees, setEmployees] = useState([])
  const [selectedEmployeeId, setSelectedEmployeeId] = useState('')
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [projectsLoading, setProjectsLoading] = useState(false)

  useEffect(() => {
    employeeService
      .getAll()
      .then((res) => {
        setEmployees(res.data)
        if (res.data.length > 0 && !selectedEmployeeId) {
          setSelectedEmployeeId(String(res.data[0].id))
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!selectedEmployeeId) {
      setProjects([])
      return
    }
    setProjectsLoading(true)
    employeeService
      .getProjects(Number(selectedEmployeeId))
      .then((res) => setProjects(res.data))
      .catch(() => setProjects([]))
      .finally(() => setProjectsLoading(false))
  }, [selectedEmployeeId])

  const selectedEmployee = employees.find((e) => String(e.id) === selectedEmployeeId)

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-luxury-earth"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-6 py-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center space-x-3 mb-2">
          <div className="bg-luxury-wasabi p-3 rounded-lg">
            <Briefcase className="w-6 h-6 text-white" />
          </div>
          <h1 className="font-display text-4xl font-bold text-luxury-white">
            My Projects
          </h1>
        </div>
        <p className="text-luxury-wasabi">View projects you are assigned to</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="luxury-card p-6 mb-6"
      >
        <label className="block text-sm font-medium text-luxury-emerald mb-2">
          I am
        </label>
        <div className="relative max-w-md">
          <select
            value={selectedEmployeeId}
            onChange={(e) => setSelectedEmployeeId(e.target.value)}
            className="luxury-select w-full pr-10 appearance-none"
          >
            <option value="">Select employee</option>
            {employees.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.name} ({emp.employee_id})
              </option>
            ))}
          </select>
          <User className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-luxury-wasabi pointer-events-none" />
        </div>
      </motion.div>

      {projectsLoading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-luxury-earth"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}

      {!projectsLoading && selectedEmployeeId && projects.length === 0 && (
        <div className="text-center py-12 text-luxury-wasabi luxury-card p-8">
          <Briefcase className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p className="text-xl">No projects assigned yet</p>
          <p className="text-sm mt-2">
            {selectedEmployee?.name}, you will see projects here once your manager confirms you on a project.
          </p>
        </div>
      )}
    </div>
  )
}

const ProjectCard = ({ project }) => {
  const complexityColors = {
    Low: 'bg-luxury-wasabi/30 text-luxury-wasabi border-luxury-wasabi/40',
    Medium: 'bg-luxury-earth/30 text-luxury-earth border-luxury-earth/40',
    High: 'bg-luxury-emerald/30 text-luxury-emerald border-luxury-emerald/40',
  }

  return (
    <Link to={`/project/${project.id}`}>
      <motion.div
        whileHover={{ scale: 1.02, y: -4 }}
        className="luxury-section p-6 h-full cursor-pointer hover:border-luxury-earth/50 transition-all"
      >
        <div className="flex items-start justify-between mb-4">
          <h3 className="font-semibold text-lg text-luxury-white">{project.name}</h3>
          <span
            className={`px-2 py-1 rounded text-xs font-medium border ${
              complexityColors[project.complexity] || complexityColors.Medium
            }`}
          >
            {project.complexity}
          </span>
        </div>
        <p className="text-luxury-wasabi text-sm mb-4 line-clamp-2">{project.description}</p>
        <div className="flex items-center justify-between text-sm">
          <span className="text-luxury-earth font-medium">{project.category}</span>
          {project.predicted_team_size && (
            <span className="text-luxury-wasabi">Team: {project.predicted_team_size}</span>
          )}
        </div>
      </motion.div>
    </Link>
  )
}

export default MyProjects
