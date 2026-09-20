import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight, TrendingUp, Users, Briefcase, Sparkles } from 'lucide-react'
import { projectService, analyticsService } from '../services/api'

const Dashboard = () => {
  const [projects, setProjects] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [projectsRes, analyticsRes] = await Promise.all([
        projectService.getAll(),
        analyticsService.getAnalytics(),
      ])
      setProjects(projectsRes.data.slice(0, 6))
      setAnalytics(analyticsRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-luxury-earth"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-6 py-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="font-display text-5xl font-bold text-luxury-white mb-2">
          Executive Dashboard
        </h1>
        <p className="text-luxury-wasabi text-lg">
          AI-powered project management with intelligent employee matching
        </p>
      </motion.div>

      {/* Stats Cards */}
      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={Briefcase}
            label="Total Projects"
            value={analytics.total_projects}
            bgColor="bg-luxury-earth"
          />
          <StatCard
            icon={Users}
            label="Total Employees"
            value={analytics.total_employees}
            bgColor="bg-luxury-wasabi"
          />
          <StatCard
            icon={TrendingUp}
            label="Avg Team Size"
            value={analytics.average_team_size.toFixed(1)}
            bgColor="bg-luxury-emerald"
          />
          <StatCard
            icon={Sparkles}
            label="AI Predictions"
            value={projects.filter(p => p.predicted_team_size).length}
            bgColor="bg-luxury-earth"
          />
        </div>
      )}

      {/* Recent Projects */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="luxury-card p-6 mb-8"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="font-display text-3xl font-bold text-luxury-white">
            Recent Projects
          </h2>
          <Link
            to="/upload"
            className="luxury-button flex items-center space-x-2"
          >
            <span>New Project</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>

        {projects.length === 0 && (
          <div className="text-center py-12 text-luxury-wasabi">
            <Briefcase className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-xl">No projects yet</p>
            <p className="text-sm mt-2">Create your first project to get started</p>
          </div>
        )}
      </motion.div>
    </div>
  )
}

const StatCard = ({ icon: Icon, label, value, bgColor }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="luxury-card p-6"
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-luxury-wasabi text-sm mb-1">{label}</p>
        <p className="text-3xl font-bold text-luxury-emerald">{value}</p>
      </div>
      <div className={`${bgColor} p-3 rounded-lg`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
    </div>
  </motion.div>
)

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
        <p className="text-luxury-wasabi text-sm mb-4 line-clamp-2">
          {project.description}
        </p>
        <div className="flex items-center justify-between text-sm">
          <span className="text-luxury-earth font-medium">{project.category}</span>
          {project.predicted_team_size && (
            <span className="text-luxury-wasabi">
              Team: {project.predicted_team_size}
            </span>
          )}
        </div>
      </motion.div>
    </Link>
  )
}

export default Dashboard
