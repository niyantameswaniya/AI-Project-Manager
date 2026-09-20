import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Upload, Sparkles, ArrowRight } from 'lucide-react'
import { projectService } from '../services/api'

const ProjectUpload = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: 'Web',
    complexity: 'Medium',
    estimated_timeline_weeks: 8,
    budget_range: '',
    client_priority: 'Medium',
    required_skills: [],
  })
  const [skillInput, setSkillInput] = useState('')
  const [skillsError, setSkillsError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validate required skills
    if (formData.required_skills.length === 0) {
      setSkillsError('Please add at least one required skill')
      return
    }
    
    setSkillsError('')
    setLoading(true)

    try {
      const response = await projectService.create(formData)
      navigate(`/project/${response.data.id}`)
    } catch (error) {
      console.error('Error creating project:', error)
      let errorMessage = 'Error creating project. Please try again.'
      
      if (error.response) {
        // Handle FastAPI validation errors
        if (error.response.data) {
          if (typeof error.response.data.detail === 'string') {
            errorMessage = error.response.data.detail
          } else if (Array.isArray(error.response.data.detail)) {
            // Handle validation error array
            const errors = error.response.data.detail.map(err => {
              if (typeof err === 'object' && err.msg) {
                return `${err.loc?.join('.') || 'Field'}: ${err.msg}`
              }
              return String(err)
            })
            errorMessage = errors.join('\n')
          } else if (typeof error.response.data === 'string') {
            errorMessage = error.response.data
          }
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      alert(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleAddSkill = () => {
    const input = skillInput.trim()
    if (!input) return
    
    // Split by comma and process each skill
    const skillsToAdd = input
      .split(',')
      .map(skill => skill.trim())
      .filter(skill => skill.length > 0)
    
    if (skillsToAdd.length === 0) return
    
    // Add each skill separately, avoiding duplicates
    const newSkills = skillsToAdd.filter(
      skill => !formData.required_skills.includes(skill)
    )
    
    if (newSkills.length > 0) {
      setFormData({
        ...formData,
        required_skills: [...formData.required_skills, ...newSkills],
      })
      setSkillsError('')
    }
    
    setSkillInput('')
  }

  const handleRemoveSkill = (skillToRemove) => {
    setFormData({
      ...formData,
      required_skills: formData.required_skills.filter(skill => skill !== skillToRemove),
    })
  }

  const handleSkillInputKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleAddSkill()
    }
  }

  return (
    <div className="container mx-auto px-6 py-8 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center space-x-3 mb-2">
          <div className="bg-luxury-earth p-3 rounded-lg">
            <Upload className="w-6 h-6 text-white" />
          </div>
          <h1 className="font-display text-4xl font-bold text-luxury-white">
            Upload New Project
          </h1>
        </div>
        <p className="text-luxury-wasabi">
          Provide project details and let AI predict the optimal team composition
        </p>
      </motion.div>

      <motion.form
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        onSubmit={handleSubmit}
        className="luxury-card p-8"
      >
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Project Name *
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className="luxury-input w-full"
              placeholder="Enter project name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Project Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows={5}
              className="luxury-textarea w-full"
              placeholder="Describe the project in detail. Include technologies, features, and requirements..."
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Project Category *
              </label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                required
                className="luxury-select w-full"
              >
                <option value="Web">Web</option>
                <option value="AI">AI</option>
                <option value="Mobile">Mobile</option>
                <option value="Automation">Automation</option>
                <option value="ERP">ERP</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Complexity Level *
              </label>
              <select
                name="complexity"
                value={formData.complexity}
                onChange={handleChange}
                required
                className="luxury-select w-full"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Estimated Timeline (weeks) *
              </label>
              <input
                type="number"
                name="estimated_timeline_weeks"
                value={formData.estimated_timeline_weeks}
                onChange={handleChange}
                required
                min="1"
                className="luxury-input w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Client Priority *
              </label>
              <select
                name="client_priority"
                value={formData.client_priority}
                onChange={handleChange}
                required
                className="luxury-select w-full"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Budget Range (optional)
            </label>
            <input
              type="text"
              name="budget_range"
              value={formData.budget_range}
              onChange={handleChange}
              className="luxury-input w-full"
              placeholder="e.g., $50k-$100k"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Required Skills *
            </label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyPress={handleSkillInputKeyPress}
                className={`luxury-input flex-1 ${skillsError ? 'border-red-500' : ''}`}
                placeholder="Enter skills (e.g., Python, React, Machine Learning or one at a time)"
              />
              <button
                type="button"
                onClick={handleAddSkill}
                className="luxury-button-secondary px-4"
              >
                Add
              </button>
            </div>
            {skillsError && (
              <p className="text-red-500 text-sm mb-2">{skillsError}</p>
            )}
            {formData.required_skills.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-2">
                {formData.required_skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-luxury-earth/30 border border-luxury-earth/50 px-3 py-1 rounded-lg text-luxury-earth flex items-center gap-2"
                  >
                    {skill}
                    <button
                      type="button"
                      onClick={() => handleRemoveSkill(skill)}
                      className="hover:text-luxury-emerald transition-colors"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            )}
            <p className="text-xs text-luxury-wasabi mt-2">
              Add at least one skill that is required for this project. You can enter multiple skills separated by commas (e.g., Python, React, Machine Learning). AI will also predict additional skills.
            </p>
          </div>
        </div>

        <div className="mt-8 flex items-center justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="px-6 py-3 border border-luxury-wasabi/40 rounded-lg text-luxury-wasabi hover:bg-luxury-emerald/20 transition-all"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="luxury-button flex items-center space-x-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                <span>Creating...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Create & Predict</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </motion.form>
    </div>
  )
}

export default ProjectUpload
