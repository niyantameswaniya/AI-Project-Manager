import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart3, TrendingUp, Users, Briefcase } from 'lucide-react'
import { analyticsService } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await analyticsService.getAnalytics()
      setAnalytics(response.data)
    } catch (error) {
      console.error('Error fetching analytics:', error)
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

  if (!analytics) {
    return <div className="container mx-auto px-6 py-8">No analytics data available</div>
  }

  const skillData = Object.entries(analytics.skill_distribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([skill, count]) => ({ skill, count }))

  const categoryData = Object.entries(analytics.category_distribution).map(([category, count]) => ({
    category,
    count,
  }))

  const COLORS = ['#B88230', '#284139', '#809078', '#1A1E24', '#111319']

  return (
    <div className="container mx-auto px-6 py-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center space-x-3 mb-2">
          <div className="bg-luxury-earth p-3 rounded-lg">
            <BarChart3 className="w-6 h-6 text-white" />
          </div>
          <h1 className="font-display text-4xl font-bold text-luxury-white">
            Analytics & Insights
          </h1>
        </div>
        <p className="text-luxury-wasabi">Comprehensive analytics and visualizations</p>
      </motion.div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard icon={Briefcase} label="Total Projects" value={analytics.total_projects} />
        <StatCard icon={Users} label="Total Employees" value={analytics.total_employees} />
        <StatCard icon={TrendingUp} label="Avg Team Size" value={analytics.average_team_size.toFixed(1)} />
        <StatCard
          icon={BarChart3}
          label="Skills Tracked"
          value={Object.keys(analytics.skill_distribution).length}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Skill Distribution */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="luxury-card p-6"
        >
          <h3 className="font-display text-2xl font-bold text-luxury-emerald mb-6">
            Top Skills Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={skillData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(128, 144, 120, 0.3)" />
              <XAxis dataKey="skill" stroke="#809078" fontSize={12} angle={-45} textAnchor="end" height={100} />
              <YAxis stroke="#809078" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1A1E24',
                  border: '1px solid rgba(184, 130, 48, 0.3)',
                  borderRadius: '8px',
                  color: '#E5E5E5',
                }}
              />
              <Bar dataKey="count" fill="#B88230" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Category Distribution */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="luxury-card p-6"
        >
          <h3 className="font-display text-2xl font-bold text-luxury-emerald mb-6">
            Project Categories
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ category, percent }) => `${category}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="count"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1A1E24',
                  border: '1px solid rgba(184, 130, 48, 0.3)',
                  borderRadius: '8px',
                  color: '#E5E5E5',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* All Skills List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="luxury-card p-6"
      >
        <h3 className="font-display text-2xl font-bold text-luxury-emerald mb-6">
          Complete Skill Inventory
        </h3>
        <div className="flex flex-wrap gap-3">
          {Object.entries(analytics.skill_distribution)
            .sort((a, b) => b[1] - a[1])
            .map(([skill, count]) => (
              <div
                key={skill}
                className="bg-luxury-earth/30 border border-luxury-earth/50 px-4 py-2 rounded-lg"
              >
                <span className="text-luxury-earth font-medium">{skill}</span>
                <span className="text-luxury-earth/70 text-sm ml-2">({count})</span>
              </div>
            ))}
        </div>
      </motion.div>
    </div>
  )
}

const StatCard = ({ icon: Icon, label, value }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="luxury-card p-6"
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-luxury-wasabi text-sm mb-1">{label}</p>
        <p className="text-3xl font-bold text-luxury-emerald">{value}</p>
      </div>
      <div className="bg-luxury-earth/20 p-3 rounded-lg">
        <Icon className="w-6 h-6 text-luxury-earth" />
      </div>
    </div>
  </motion.div>
)

export default Analytics
