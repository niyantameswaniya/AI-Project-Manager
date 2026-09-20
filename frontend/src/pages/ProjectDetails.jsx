import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Sparkles, Users, TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react'
import { projectService } from '../services/api'

const ProjectDetails = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [project, setProject] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)
  const [predicting, setPredicting] = useState(false)

  useEffect(() => {
    fetchProject()
  }, [id])

  const [confirming, setConfirming] = useState(false)

  const fetchProject = async () => {
    try {
      const response = await projectService.getById(id)
      setProject(response.data)
      if (response.data.predicted_team_size) {
        fetchPrediction()
      }
    } catch (error) {
      console.error('Error fetching project:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleConfirmEmployee = async (employeeDbId) => {
    const assigned = project?.assigned_employee_ids || []
    if (assigned.includes(employeeDbId)) return
    setConfirming(true)
    try {
      await projectService.assign(id, [...assigned, employeeDbId])
      await fetchProject()
    } catch (error) {
      console.error('Error confirming employee:', error)
      alert('Failed to confirm employee.')
    } finally {
      setConfirming(false)
    }
  }

  const handleConfirmMultiple = async (employeeDbIds) => {
    const assigned = project?.assigned_employee_ids || []
    const toAdd = employeeDbIds.filter((eid) => !assigned.includes(eid))
    if (toAdd.length === 0) return
    setConfirming(true)
    try {
      await projectService.assign(id, [...assigned, ...toAdd])
      await fetchProject()
    } catch (error) {
      console.error('Error confirming employees:', error)
      alert('Failed to confirm employees.')
    } finally {
      setConfirming(false)
    }
  }

  const fetchPrediction = async () => {
    try {
      const response = await projectService.predict(id)
      setPrediction(response.data)
    } catch (error) {
      console.error('Error fetching prediction:', error)
    }
  }

  const handlePredict = async () => {
    setPredicting(true)
    try {
      const response = await projectService.predict(id)
      setPrediction(response.data)
      const projectResponse = await projectService.getById(id)
      setProject(projectResponse.data)
    } catch (error) {
      console.error('Error generating prediction:', error)
      alert('Error generating prediction. Please try again.')
    } finally {
      setPredicting(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-luxury-earth"></div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="container mx-auto px-6 py-8">
        <p className="text-luxury-wasabi">Project not found</p>
      </div>
    )
  }

  const complexityColors = {
    Low: 'bg-luxury-wasabi/30 text-luxury-wasabi border-luxury-wasabi/40',
    Medium: 'bg-luxury-earth/30 text-luxury-earth border-luxury-earth/40',
    High: 'bg-luxury-emerald/30 text-luxury-emerald border-luxury-emerald/40',
  }

  return (
    <div className="container mx-auto px-6 py-8 max-w-7xl">
      <button
        onClick={() => navigate('/')}
        className="flex items-center space-x-2 text-luxury-wasabi hover:text-luxury-white mb-6 transition-colors"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Dashboard</span>
      </button>

      {/* Project Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="luxury-card p-8 mb-6"
      >
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="font-display text-4xl font-bold text-luxury-emerald mb-2">
              {project.name}
            </h1>
            <p className="text-luxury-wasabi">{project.description}</p>
          </div>
          <span
            className={`px-4 py-2 rounded-lg border font-medium ${
              complexityColors[project.complexity] || complexityColors.Medium
            }`}
          >
            {project.complexity}
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <InfoCard label="Category" value={project.category} />
          <InfoCard label="Timeline" value={`${project.estimated_timeline_weeks} weeks`} />
          <InfoCard label="Priority" value={project.client_priority} />
          {project.budget_range && (
            <InfoCard label="Budget" value={project.budget_range} />
          )}
        </div>

        {project.required_skills && project.required_skills.length > 0 && (
          <div className="mt-4">
            <p className="text-sm text-luxury-wasabi mb-2">User-Provided Required Skills:</p>
            <div className="flex flex-wrap gap-2">
              {project.required_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="bg-luxury-earth/30 border border-luxury-earth/50 px-3 py-1 rounded-lg text-luxury-earth"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </motion.div>

      {/* Prediction Section */}
      {!prediction && !project.predicted_team_size && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="luxury-section p-8 text-center"
        >
          <Sparkles className="w-16 h-16 text-luxury-earth mx-auto mb-4" />
          <h2 className="font-display text-2xl font-bold text-luxury-white mb-2">
            Generate AI Predictions
          </h2>
          <p className="text-luxury-wasabi mb-6">
            Let our ML models predict the optimal team size, required skills, and best-fit employees
          </p>
          <button
            onClick={handlePredict}
            disabled={predicting}
            className="luxury-button flex items-center space-x-2 mx-auto disabled:opacity-50"
          >
            {predicting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Generate Predictions</span>
              </>
            )}
          </button>
        </motion.div>
      )}

      {/* Prediction Results */}
      {prediction && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Prediction Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="luxury-card p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg text-luxury-emerald">Team Size</h3>
                <Users className="w-6 h-6 text-luxury-earth" />
              </div>
              <p className="text-4xl font-bold text-luxury-earth">
                {prediction.predicted_team_size}
              </p>
              <p className="text-sm text-luxury-wasabi mt-2">predicted employees</p>
            </div>

            <div className="luxury-card p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg text-luxury-emerald">Confidence</h3>
                <TrendingUp className="w-6 h-6 text-luxury-earth" />
              </div>
              <div className="relative w-24 h-24 mx-auto">
                <svg className="transform -rotate-90 w-24 h-24">
                  <circle
                    cx="48"
                    cy="48"
                    r="40"
                    stroke="rgba(128, 144, 120, 0.3)"
                    strokeWidth="8"
                    fill="none"
                  />
                  <circle
                    cx="48"
                    cy="48"
                    r="40"
                    stroke="#B88230"
                    strokeWidth="8"
                    fill="none"
                    strokeDasharray={`${2 * Math.PI * 40}`}
                    strokeDashoffset={`${2 * Math.PI * 40 * (1 - prediction.confidence_score / 100)}`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-2xl font-bold text-luxury-earth">
                    {prediction.confidence_score.toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>

            <div className="luxury-card p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg text-luxury-emerald">Required Skills</h3>
                <Sparkles className="w-6 h-6 text-luxury-earth" />
              </div>
              <p className="text-4xl font-bold text-luxury-earth">
                {(() => {
                  const userSkills = project.required_skills || []
                  const mlSkills = prediction.predicted_skills || []
                  const allSkills = new Set([...userSkills, ...mlSkills.map(s => s.skill)])
                  return allSkills.size
                })()}
              </p>
              <p className="text-sm text-luxury-wasabi mt-2">skills identified</p>
            </div>
          </div>

          {/* Skills List */}
          <div className="luxury-card p-6">
            <h3 className="font-display text-2xl font-bold text-luxury-emerald mb-4">
              Required Skills
            </h3>
            
            {/* User-Provided Skills */}
            {project.required_skills && project.required_skills.length > 0 && (
              <div className="mb-6">
                <h4 className="text-sm font-semibold text-luxury-wasabi mb-3">
                  User-Provided Skills:
                </h4>
                <div className="flex flex-wrap gap-3">
                  {project.required_skills.map((skill, idx) => (
                    <motion.div
                      key={`user-${idx}`}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: idx * 0.05 }}
                      className="bg-luxury-earth/30 border border-luxury-earth/50 px-4 py-2 rounded-lg"
                    >
                      <span className="text-luxury-earth font-medium">{skill}</span>
                      <span className="text-luxury-earth/70 text-sm ml-2">(User)</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* ML-Predicted Skills */}
            {prediction.predicted_skills && prediction.predicted_skills.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-luxury-wasabi mb-3">
                  AI-Predicted Skills:
                </h4>
                <div className="flex flex-wrap gap-3">
                  {prediction.predicted_skills.map((skill, idx) => (
                    <motion.div
                      key={`ml-${idx}`}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: (project.required_skills?.length || 0) * 0.05 + idx * 0.05 }}
                      className="bg-luxury-earth/30 border border-luxury-earth/50 px-4 py-2 rounded-lg"
                    >
                      <span className="text-luxury-earth font-medium">{skill.skill}</span>
                      <span className="text-luxury-earth/70 text-sm ml-2">
                        ({skill.confidence}%)
                      </span>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {/* Show message if no skills */}
            {(!project.required_skills || project.required_skills.length === 0) && 
             (!prediction.predicted_skills || prediction.predicted_skills.length === 0) && (
              <p className="text-luxury-wasabi">No skills identified yet. Generate predictions to see AI-suggested skills.</p>
            )}
          </div>

          {/* Employee Recommendations + Confirm (Manager) */}
          <div className="luxury-card p-6">
            <h3 className="font-display text-2xl font-bold text-luxury-emerald mb-2">
              Recommended Employees
            </h3>
            <p className="text-sm text-luxury-wasabi mb-6">
              Confirm employees to assign them to this project. Confirmed employees will see this project under My Projects.
            </p>
            <div className="space-y-4">
              {prediction.recommended_employees.map((emp, idx) => (
                <EmployeeCard
                  key={idx}
                  employee={emp}
                  index={idx}
                  isConfirmed={(project.assigned_employee_ids || []).includes(emp.employee_id)}
                  onConfirm={() => handleConfirmEmployee(emp.employee_id)}
                  confirming={confirming}
                />
              ))}
            </div>
          </div>

          {/* Missing Skills - Only show if there are truly missing skills not covered by any employee */}
          {prediction.missing_skills && prediction.missing_skills.length > 0 && (
            <div className="luxury-section p-6 border border-luxury-wasabi/50">
              <div className="flex items-center space-x-3 mb-4">
                <AlertCircle className="w-6 h-6 text-luxury-wasabi" />
                <h3 className="font-display text-xl font-bold text-luxury-wasabi">
                  Skills Not Covered
                </h3>
              </div>
              <p className="text-sm text-luxury-wasabi mb-3">
                These skills are not available in the recommended team. Consider adding more employees or training.
              </p>
              <div className="flex flex-wrap gap-3">
                {prediction.missing_skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-luxury-wasabi/30 border border-luxury-wasabi/40 px-4 py-2 rounded-lg text-luxury-wasabi"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Explanation */}
          <div className="luxury-card p-6">
            <div className="flex items-center space-x-3 mb-4">
              <CheckCircle2 className="w-6 h-6 text-luxury-earth" />
              <h3 className="font-display text-xl font-bold text-luxury-emerald">
                AI Explanation
              </h3>
            </div>
            <p className="text-luxury-wasabi leading-relaxed">{prediction.explanation}</p>
          </div>
        </motion.div>
      )}
    </div>
  )
}

const InfoCard = ({ label, value }) => (
  <div>
    <p className="text-sm text-luxury-wasabi mb-1">{label}</p>
    <p className="text-lg font-semibold text-luxury-emerald">{value}</p>
  </div>
)

const EmployeeCard = ({ employee, index, isConfirmed, onConfirm, confirming }) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className={`luxury-section p-6 hover:border-luxury-earth/50 transition-all ${isConfirmed ? 'border-luxury-wasabi/40' : ''}`}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="flex items-center gap-2">
            <h4 className="font-semibold text-lg text-luxury-white mb-1">{employee.employee_name}</h4>
            {isConfirmed && (
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-luxury-wasabi/30 text-luxury-wasabi border border-luxury-wasabi/50">
                Confirmed
              </span>
            )}
          </div>
          <p className="text-sm text-luxury-wasabi">ID: {employee.employee_employee_id}</p>
        </div>
        <div className="text-right flex items-center gap-4">
          <div>
            <div className="text-2xl font-bold text-luxury-earth">
              {employee.match_score.toFixed(0)}%
            </div>
            <p className="text-xs text-luxury-wasabi">Match Score</p>
          </div>
          {!isConfirmed && (
            <button
              type="button"
              onClick={onConfirm}
              disabled={confirming}
              className="luxury-button px-4 py-2 text-sm disabled:opacity-50"
            >
              {confirming ? '...' : 'Confirm'}
            </button>
          )}
        </div>
      </div>

      <div className="mb-4">
        <p className="text-sm text-luxury-wasabi mb-2">Match Reason:</p>
        <p className="text-sm text-luxury-grey">{employee.match_reason}</p>
      </div>

      {employee.skills_match.length > 0 && (
        <div className="mb-4">
          <p className="text-sm text-luxury-wasabi mb-2">Matching Skills:</p>
          <div className="flex flex-wrap gap-2">
            {employee.skills_match.map((skill, idx) => (
              <span
                key={idx}
                className="bg-luxury-wasabi/30 border border-luxury-wasabi/40 px-3 py-1 rounded text-sm text-luxury-wasabi"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {employee.missing_skills.length > 0 && (
        <div>
          <p className="text-sm text-luxury-wasabi mb-2">Missing Skills:</p>
          <div className="flex flex-wrap gap-2">
            {employee.missing_skills.map((skill, idx) => (
              <span
                key={idx}
                className="bg-luxury-earth/30 border border-luxury-earth/40 px-3 py-1 rounded text-sm text-luxury-earth"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default ProjectDetails
