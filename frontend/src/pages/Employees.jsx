import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Users, Star, Clock, TrendingUp, ArrowRight } from 'lucide-react'
import { employeeService } from '../services/api'

const Employees = () => {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEmployees()
  }, [])

  const fetchEmployees = async () => {
    try {
      const response = await employeeService.getAll()
      setEmployees(response.data)
    } catch (error) {
      console.error('Error fetching employees:', error)
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
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-3">
            <div className="bg-luxury-earth p-3 rounded-lg">
              <Users className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-display text-4xl font-bold text-luxury-white">
                Employee Database
              </h1>
              <p className="text-luxury-wasabi">View and manage all employees in the system</p>
            </div>
          </div>
          <Link
            to="/employees/upload"
            className="luxury-button flex items-center space-x-2"
          >
            <span>New Employee</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {employees.map((employee, idx) => (
          <EmployeeCard key={employee.id} employee={employee} index={idx} />
        ))}
      </div>

      {employees.length === 0 && (
        <div className="text-center py-12 text-luxury-wasabi">
          <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p className="text-xl">No employees found</p>
        </div>
      )}
    </div>
  )
}

const EmployeeCard = ({ employee, index }) => {
  const avgProficiency =
    employee.skill_proficiency.reduce((a, b) => a + b, 0) / employee.skill_proficiency.length

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      whileHover={{ scale: 1.02, y: -4 }}
      className="luxury-card p-6"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-semibold text-lg text-luxury-emerald mb-1">{employee.name}</h3>
          <p className="text-sm text-luxury-wasabi">ID: {employee.employee_id}</p>
        </div>
        <div className="text-right">
          <div className="flex items-center space-x-1 text-luxury-earth mb-1">
            <Star className="w-4 h-4 fill-luxury-earth" />
            <span className="font-semibold">{employee.performance_score.toFixed(1)}</span>
          </div>
          <p className="text-xs text-luxury-wasabi">Performance</p>
        </div>
      </div>

      <div className="space-y-3 mb-4">
        <div className="flex items-center space-x-2 text-sm">
          <Clock className="w-4 h-4 text-luxury-wasabi" />
          <span className="text-luxury-grey">
            {employee.years_of_experience} years experience
          </span>
        </div>
        <div className="flex items-center space-x-2 text-sm">
          <TrendingUp className="w-4 h-4 text-luxury-wasabi" />
          <span className="text-luxury-grey">
            {employee.availability_percent}% available
          </span>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-xs text-luxury-wasabi mb-2">Skills ({employee.skills.length}):</p>
        <div className="flex flex-wrap gap-2">
          {employee.skills.slice(0, 5).map((skill, idx) => (
            <span
              key={idx}
              className="bg-luxury-earth/30 border border-luxury-earth/40 px-2 py-1 rounded text-xs text-luxury-earth"
            >
              {skill}
            </span>
          ))}
          {employee.skills.length > 5 && (
            <span className="text-xs text-luxury-wasabi">+{employee.skills.length - 5} more</span>
          )}
        </div>
      </div>

      {employee.past_project_types && employee.past_project_types.length > 0 && (
        <div>
          <p className="text-xs text-luxury-wasabi mb-2">Past Projects:</p>
          <div className="flex flex-wrap gap-2">
            {employee.past_project_types.map((type, idx) => (
              <span
                key={idx}
                className="bg-luxury-wasabi/30 border border-luxury-wasabi/40 px-2 py-1 rounded text-xs text-luxury-wasabi"
              >
                {type}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default Employees
