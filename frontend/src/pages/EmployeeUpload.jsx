import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UserPlus, ArrowRight, X } from 'lucide-react'
import { employeeService } from '../services/api'

const EmployeeUpload = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    employee_id: '',
    name: '',
    email: '',
    department: '',
    location: '',
    designation: '',
    skills: [],
    skill_proficiency: [],
    skill_types: [],
    years_of_experience: 0,
    past_project_types: [],
    certifications: [],
    education: '',
    availability_percent: 100,
    performance_score: 5.0,
    hourly_rate: '',
    languages: [],
    frameworks: [],
    domain_expertise: [],
  })
  const [skillInput, setSkillInput] = useState('')
  const [proficiencyInput, setProficiencyInput] = useState('')
  const [errors, setErrors] = useState({})

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validate required fields
    const newErrors = {}
    if (!formData.employee_id.trim()) {
      newErrors.employee_id = 'Employee ID is required'
    }
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    }
    if (formData.skills.length === 0) {
      newErrors.skills = 'At least one skill is required'
    }
    if (formData.skills.length !== formData.skill_proficiency.length) {
      newErrors.skills = 'Each skill must have a proficiency level'
    }
    if (formData.years_of_experience < 0) {
      newErrors.years_of_experience = 'Years of experience must be 0 or greater'
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    
    setErrors({})
    setLoading(true)

    // Prepare data for API
    const submitData = {
      ...formData,
      hourly_rate: formData.hourly_rate ? parseFloat(formData.hourly_rate) : null,
      years_of_experience: parseFloat(formData.years_of_experience),
      availability_percent: parseFloat(formData.availability_percent),
      performance_score: parseFloat(formData.performance_score),
    }

    try {
      const response = await employeeService.create(submitData)
      navigate('/employees')
    } catch (error) {
      console.error('Error creating employee:', error)
      let errorMessage = 'Error creating employee. Please try again.'
      
      if (error.response) {
        if (error.response.data) {
          if (typeof error.response.data.detail === 'string') {
            errorMessage = error.response.data.detail
          } else if (Array.isArray(error.response.data.detail)) {
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
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value,
    })
    // Clear error for this field
    if (errors[name]) {
      setErrors({ ...errors, [name]: '' })
    }
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
    
    const proficiency = proficiencyInput.trim() ? parseInt(proficiencyInput) : 3
    if (isNaN(proficiency) || proficiency < 1 || proficiency > 5) {
      setErrors({ ...errors, skills: 'Proficiency must be between 1 and 5' })
      return
    }
    
    // Add each skill with the same proficiency
    const newSkills = skillsToAdd.filter(
      skill => !formData.skills.includes(skill)
    )
    
    if (newSkills.length > 0) {
      setFormData({
        ...formData,
        skills: [...formData.skills, ...newSkills],
        skill_proficiency: [...formData.skill_proficiency, ...newSkills.map(() => proficiency)],
        skill_types: [...formData.skill_types, ...newSkills.map(() => 'Technical')],
      })
      setErrors({ ...errors, skills: '' })
    }
    
    setSkillInput('')
    setProficiencyInput('')
  }

  const handleRemoveSkill = (index) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter((_, i) => i !== index),
      skill_proficiency: formData.skill_proficiency.filter((_, i) => i !== index),
      skill_types: formData.skill_types.filter((_, i) => i !== index),
    })
  }

  const handleSkillInputKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleAddSkill()
    }
  }

  const handleAddArrayItem = (fieldName, value) => {
    if (value.trim()) {
      setFormData({
        ...formData,
        [fieldName]: [...formData[fieldName], value.trim()],
      })
    }
  }

  const handleRemoveArrayItem = (fieldName, index) => {
    setFormData({
      ...formData,
      [fieldName]: formData[fieldName].filter((_, i) => i !== index),
    })
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
            <UserPlus className="w-6 h-6 text-white" />
          </div>
          <h1 className="font-display text-4xl font-bold text-luxury-white">
            Add New Employee
          </h1>
        </div>
        <p className="text-luxury-wasabi">
          Add employee details to the database
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
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Employee ID *
              </label>
              <input
                type="text"
                name="employee_id"
                value={formData.employee_id}
                onChange={handleChange}
                required
                className={`luxury-input w-full ${errors.employee_id ? 'border-red-500' : ''}`}
                placeholder="e.g., EMP001"
              />
              {errors.employee_id && (
                <p className="text-red-500 text-xs mt-1">{errors.employee_id}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className={`luxury-input w-full ${errors.name ? 'border-red-500' : ''}`}
                placeholder="Full name"
              />
              {errors.name && (
                <p className="text-red-500 text-xs mt-1">{errors.name}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Email
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="luxury-input w-full"
                placeholder="email@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Department
              </label>
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                className="luxury-input w-full"
                placeholder="e.g., Engineering"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Location
              </label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className="luxury-input w-full"
                placeholder="e.g., San Francisco"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Designation
            </label>
            <input
              type="text"
              name="designation"
              value={formData.designation}
              onChange={handleChange}
              className="luxury-input w-full"
              placeholder="e.g., Senior Developer"
            />
          </div>

          {/* Skills Section */}
          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Skills * (with Proficiency 1-5)
            </label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyPress={handleSkillInputKeyPress}
                className={`luxury-input flex-1 ${errors.skills ? 'border-red-500' : ''}`}
                placeholder="Enter skills (e.g., Python, React, Machine Learning)"
              />
              <input
                type="number"
                value={proficiencyInput}
                onChange={(e) => setProficiencyInput(e.target.value)}
                className="luxury-input w-24"
                placeholder="1-5"
                min="1"
                max="5"
              />
              <button
                type="button"
                onClick={handleAddSkill}
                className="luxury-button-secondary px-4"
              >
                Add
              </button>
            </div>
            {errors.skills && (
              <p className="text-red-500 text-sm mb-2">{errors.skills}</p>
            )}
            {formData.skills.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-2">
                {formData.skills.map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-luxury-earth/30 border border-luxury-earth/50 px-3 py-1 rounded-lg text-luxury-earth flex items-center gap-2"
                  >
                    {skill} ({formData.skill_proficiency[idx]}/5)
                    <button
                      type="button"
                      onClick={() => handleRemoveSkill(idx)}
                      className="hover:text-luxury-emerald transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </span>
                ))}
              </div>
            )}
            <p className="text-xs text-luxury-wasabi mt-2">
              Add skills separated by commas. Proficiency: 1=Beginner, 5=Expert
            </p>
          </div>

          {/* Experience & Performance */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Years of Experience *
              </label>
              <input
                type="number"
                name="years_of_experience"
                value={formData.years_of_experience}
                onChange={handleChange}
                required
                min="0"
                step="0.5"
                className={`luxury-input w-full ${errors.years_of_experience ? 'border-red-500' : ''}`}
              />
              {errors.years_of_experience && (
                <p className="text-red-500 text-xs mt-1">{errors.years_of_experience}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Availability (%)
              </label>
              <input
                type="number"
                name="availability_percent"
                value={formData.availability_percent}
                onChange={handleChange}
                min="0"
                max="100"
                className="luxury-input w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-luxury-emerald mb-2">
                Performance Score (1-10)
              </label>
              <input
                type="number"
                name="performance_score"
                value={formData.performance_score}
                onChange={handleChange}
                min="1"
                max="10"
                step="0.1"
                className="luxury-input w-full"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Education
            </label>
            <input
              type="text"
              name="education"
              value={formData.education}
              onChange={handleChange}
              className="luxury-input w-full"
              placeholder="e.g., B.S. Computer Science"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-luxury-emerald mb-2">
              Hourly Rate (optional)
            </label>
            <input
              type="number"
              name="hourly_rate"
              value={formData.hourly_rate}
              onChange={handleChange}
              min="0"
              step="0.01"
              className="luxury-input w-full"
              placeholder="e.g., 50.00"
            />
          </div>
        </div>

        <div className="mt-8 flex items-center justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/employees')}
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
                <UserPlus className="w-5 h-5" />
                <span>Create Employee</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </motion.form>
    </div>
  )
}

export default EmployeeUpload
