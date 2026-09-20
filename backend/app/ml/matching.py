"""Employee matching engine using similarity and scoring"""
import numpy as np
from typing import List, Dict, Tuple, Set
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from ..models import Employee


class EmployeeMatchingEngine:
    """Engine for matching employees to projects based on skills and other factors"""
    
    # Skill aliases and synonyms mapping
    SKILL_ALIASES = {
        # Machine Learning variations
        'machine learning': ['ml', 'machinelearning', 'ml engineering', 'ml engineer'],
        'ml': ['machine learning', 'machinelearning', 'ml engineering'],
        'deep learning': ['dl', 'deeplearning', 'neural networks', 'neural nets'],
        'dl': ['deep learning', 'deeplearning'],
        'artificial intelligence': ['ai', 'artificialintelligence'],
        'ai': ['artificial intelligence', 'artificialintelligence'],
        
        # Programming languages
        'javascript': ['js', 'ecmascript'],
        'js': ['javascript', 'ecmascript'],
        'typescript': ['ts'],
        'ts': ['typescript'],
        'c++': ['cpp', 'cplusplus', 'c plus plus'],
        'cpp': ['c++', 'cplusplus'],
        'c#': ['csharp', 'c sharp'],
        'csharp': ['c#', 'c sharp'],
        
        # Frameworks and tools
        'react': ['reactjs', 'react.js'],
        'reactjs': ['react', 'react.js'],
        'node.js': ['nodejs', 'node', 'nodejs'],
        'nodejs': ['node.js', 'node'],
        'vue.js': ['vuejs', 'vue'],
        'vuejs': ['vue.js', 'vue'],
        'angular': ['angularjs', 'angular.js'],
        'angularjs': ['angular', 'angular.js'],
        
        # Databases
        'postgresql': ['postgres', 'pg'],
        'postgres': ['postgresql', 'pg'],
        'mongodb': ['mongo', 'nosql'],
        'mongo': ['mongodb', 'nosql'],
        'mysql': ['mysql database'],
        
        # Cloud platforms
        'amazon web services': ['aws', 'amazon aws'],
        'aws': ['amazon web services', 'amazon aws'],
        'google cloud platform': ['gcp', 'google cloud'],
        'gcp': ['google cloud platform', 'google cloud'],
        'microsoft azure': ['azure', 'ms azure'],
        'azure': ['microsoft azure', 'ms azure'],
        
        # DevOps and tools
        'continuous integration': ['ci', 'ci/cd'],
        'ci': ['continuous integration', 'ci/cd'],
        'continuous deployment': ['cd', 'ci/cd'],
        'cd': ['continuous deployment', 'ci/cd'],
        'docker': ['docker containerization'],
        'kubernetes': ['k8s', 'kube'],
        'k8s': ['kubernetes', 'kube'],
        
        # Data and analytics
        'data analysis': ['data analytics', 'data science'],
        'data science': ['data analysis', 'data analytics'],
        'business intelligence': ['bi', 'business analytics'],
        'bi': ['business intelligence', 'business analytics'],
        
        # UI/UX
        'ui/ux design': ['ui design', 'ux design', 'ui ux', 'user interface', 'user experience'],
        'ui design': ['ui/ux design', 'ux design', 'user interface'],
        'ux design': ['ui/ux design', 'ui design', 'user experience'],
        
        # Mobile
        'ios': ['iphone os', 'apple ios'],
        'android': ['android development', 'android os'],
        'react native': ['reactnative', 'rn'],
        'reactnative': ['react native', 'rn'],
        'rn': ['react native', 'reactnative'],
        
        # Automation
        'robotic process automation': ['rpa', 'process automation'],
        'rpa': ['robotic process automation', 'process automation'],
        'test automation': ['automated testing', 'qa automation'],
        'selenium': ['selenium webdriver', 'selenium testing'],
        
        # ERP
        'sap': ['sap erp', 'sap systems'],
        'oracle': ['oracle erp', 'oracle systems'],
        'erp systems': ['erp', 'enterprise resource planning'],
        'erp': ['erp systems', 'enterprise resource planning'],
    }
    
    def __init__(self):
        pass
    
    def expand_skill_aliases(self, skill: str) -> Set[str]:
        """Expand a skill with its aliases and variations"""
        skill_lower = skill.lower().strip()
        aliases = {skill_lower, skill.strip()}  # Include original
        
        # Add direct aliases
        if skill_lower in self.SKILL_ALIASES:
            aliases.update([a.lower() for a in self.SKILL_ALIASES[skill_lower]])
        
        # Check reverse mapping (if skill is an alias of something else)
        for main_skill, alias_list in self.SKILL_ALIASES.items():
            if skill_lower in [a.lower() for a in alias_list]:
                aliases.add(main_skill.lower())
                aliases.update([a.lower() for a in alias_list])
        
        # Add word variations (remove spaces, hyphens, etc.)
        aliases.add(skill_lower.replace(' ', '').replace('-', '').replace('_', '').replace('/', ''))
        
        return aliases
    
    def normalize_skill_for_matching(self, skill: str) -> Set[str]:
        """Normalize skill and return all possible variations"""
        skill_lower = skill.lower().strip()
        variations = {skill_lower}
        
        # Expand with aliases
        variations.update(self.expand_skill_aliases(skill))
        
        # Add common variations
        # Remove common words
        words_to_remove = ['the', 'and', 'or', 'of', 'for', 'with']
        words = skill_lower.split()
        if len(words) > 1:
            filtered_words = [w for w in words if w not in words_to_remove]
            if filtered_words:
                variations.add(' '.join(filtered_words))
                variations.add(''.join(filtered_words))
        
        # Add acronym version (first letters of words)
        if ' ' in skill_lower:
            acronym = ''.join([w[0] for w in skill_lower.split() if w])
            if len(acronym) >= 2:
                variations.add(acronym)
        
        return variations
    
    def calculate_skill_match(self, required_skills: List[str], employee_skills: List[str], 
                            employee_proficiencies: List[int], skill_types: List[str] = None) -> Tuple[float, List[str], List[str]]:
        """Calculate skill match percentage and identify matching/missing skills with alias support"""
        if not required_skills:
            return 0.0, [], []
        
        # Expand all required skills with their aliases
        required_skill_variations = {}
        for req_skill in required_skills:
            variations = self.normalize_skill_for_matching(req_skill)
            required_skill_variations[req_skill] = variations
        
        # Expand all employee skills with their aliases
        employee_skill_variations = {}
        for emp_skill in employee_skills:
            variations = self.normalize_skill_for_matching(emp_skill)
            employee_skill_variations[emp_skill] = variations
        
        # Find matching skills using alias-aware matching
        # Map: required_skill -> (employee_skill_index, employee_skill_name)
        skill_matches = {}  # Maps required skill to matched employee skill
        employee_skill_to_index = {}  # Maps employee skill name to its index
        
        # Build employee skill index map
        for i, emp_skill in enumerate(employee_skills):
            if emp_skill not in employee_skill_to_index:
                employee_skill_to_index[emp_skill] = i
        
        # Match each required skill to best employee skill
        for req_skill in required_skills:
            req_variations = required_skill_variations[req_skill]
            best_match_skill = None
            best_match_idx = -1
            best_match_score = 0.0
            
            for emp_skill in employee_skills:
                emp_variations = employee_skill_variations[emp_skill]
                
                # Check for any overlap between variations
                overlap = req_variations.intersection(emp_variations)
                if overlap:
                    # Calculate match score
                    req_lower = req_skill.lower().strip()
                    emp_lower = emp_skill.lower().strip()
                    
                    if req_lower == emp_lower:
                        score = 1.0  # Exact match
                    elif req_lower in emp_lower or emp_lower in req_lower:
                        score = 0.9  # Substring match
                    elif overlap:
                        score = 0.8  # Alias match
                    else:
                        score = 0.6  # Partial match
                    
                    if score > best_match_score:
                        best_match_skill = emp_skill
                        best_match_idx = employee_skill_to_index[emp_skill]
                        best_match_score = score
            
            if best_match_skill:
                skill_matches[req_skill] = (best_match_idx, best_match_skill)
        
        # Build matching_skills list (unique employee skills only)
        # Use a set with case-insensitive comparison to ensure uniqueness
        seen_skills_lower = set()
        matching_skills = []
        matching_skill_indices = []
        
        # Process skill_matches to get unique employee skills
        for req_skill, (emp_idx, emp_skill) in skill_matches.items():
            emp_skill_lower = emp_skill.lower().strip()
            if emp_skill_lower not in seen_skills_lower:
                matching_skills.append(emp_skill)  # Use original case from employee
                matching_skill_indices.append(emp_idx)
                seen_skills_lower.add(emp_skill_lower)
        
        # Final deduplication pass (in case of any edge cases)
        final_matching_skills = []
        final_seen = set()
        for skill in matching_skills:
            skill_lower = skill.lower().strip()
            if skill_lower not in final_seen:
                final_matching_skills.append(skill)
                final_seen.add(skill_lower)
        
        matching_skills = final_matching_skills
        
        # Get proficiencies and types for matched skills
        matching_proficiencies = []
        matching_types = []
        for emp_idx in matching_skill_indices:
            if emp_idx < len(employee_proficiencies):
                matching_proficiencies.append(employee_proficiencies[emp_idx])
            if skill_types and emp_idx < len(skill_types):
                matching_types.append(skill_types[emp_idx])
        
        # Find missing skills (those that didn't match)
        matched_required_skills = set(skill_matches.keys())
        missing_skills = [s for s in required_skills if s not in matched_required_skills]
        
        # Calculate match percentage with proficiency weighting
        if not required_skills:
            match_percentage = 0.0
        else:
            base_match = len(matching_skills) / len(required_skills)
            
            # Weight by proficiency (if skills match, boost score based on proficiency)
            proficiency_boost = 0.0
            if matching_proficiencies:
                avg_proficiency = np.mean(matching_proficiencies)
                proficiency_boost = (avg_proficiency - 1) / 4.0  # Normalize 1-5 to 0-1
            
            # Bonus for technical skills match
            type_bonus = 0.0
            if matching_types:
                technical_count = sum(1 for t in matching_types if t and 'technical' in t.lower())
                if technical_count > 0:
                    type_bonus = min(0.1, technical_count * 0.02)
            
            match_percentage = min(1.0, base_match * 0.65 + proficiency_boost * 0.3 + type_bonus)
        
        return match_percentage, matching_skills, missing_skills
    
    def calculate_experience_relevance(self, project_category: str, 
                                     past_project_types: List[str],
                                     domain_expertise: List[str] = None) -> float:
        """Calculate how relevant employee's experience is to project category"""
        score = 0.0
        project_lower = project_category.lower()
        
        # Check past project types
        if past_project_types:
            past_lower = [p.lower() for p in past_project_types]
            if project_lower in past_lower:
                score += 0.6
            else:
                # Partial match
                for past in past_lower:
                    if project_lower in past or past in project_lower:
                        score += 0.4
                        break
        
        # Check domain expertise
        if domain_expertise:
            # If employee has relevant domain expertise, boost score
            # This is a simplified check - in production, use more sophisticated matching
            score += 0.2
        
        return min(1.0, score) if score > 0 else 0.3
    
    def calculate_certification_bonus(self, required_skills: List[str],
                                     certifications: List[str] = None) -> float:
        """Calculate bonus score based on relevant certifications"""
        if not certifications or not required_skills:
            return 0.0
        
        bonus = 0.0
        cert_lower = [c.lower() for c in certifications]
        skills_lower = [s.lower() for s in required_skills]
        
        # Check if certifications match required skills
        for skill in skills_lower:
            for cert in cert_lower:
                if skill in cert or cert in skill:
                    bonus += 0.05
        
        return min(0.15, bonus)  # Max 15% bonus
    
    def calculate_match_score(self, employee: Employee, required_skills: List[str],
                            project_category: str, project_complexity: str) -> Tuple[float, str]:
        """Calculate overall match score for an employee with enhanced factors"""
        # Skill match (40% weight) - most important
        skill_match, matching_skills, missing_skills = self.calculate_skill_match(
            required_skills, 
            employee.skills, 
            employee.skill_proficiency,
            employee.skill_types or []
        )
        
        # Experience relevance (20% weight)
        experience_relevance = self.calculate_experience_relevance(
            project_category, 
            employee.past_project_types or [],
            employee.domain_expertise or []
        )
        
        # Availability (15% weight) - higher availability = better match
        availability_score = employee.availability_percent / 100.0
        
        # Performance (15% weight) - normalize 1-10 to 0-1
        performance_score = (employee.performance_score - 1) / 9.0
        
        # Certification bonus (5% weight)
        cert_bonus = self.calculate_certification_bonus(
            required_skills,
            employee.certifications or []
        )
        
        # Experience level match (5% weight) - match experience to complexity
        complexity_experience_map = {
            'Low': 2.0,    # 2+ years
            'Medium': 5.0,  # 5+ years
            'High': 8.0     # 8+ years
        }
        required_exp = complexity_experience_map.get(project_complexity, 5.0)
        if employee.years_of_experience >= required_exp:
            experience_level_score = 1.0
        else:
            experience_level_score = employee.years_of_experience / required_exp
        
        # Calculate weighted score
        total_score = (
            skill_match * 0.40 +
            experience_relevance * 0.20 +
            availability_score * 0.15 +
            performance_score * 0.15 +
            cert_bonus +
            experience_level_score * 0.05
        )
        
        # Generate detailed explanation
        reasons = []
        if skill_match > 0.7:
            reasons.append(f"Strong skill match ({len(matching_skills)}/{len(required_skills)} skills)")
        elif skill_match > 0.4:
            reasons.append(f"Moderate skill match ({len(matching_skills)}/{len(required_skills)} skills)")
        
        if experience_relevance > 0.7:
            reasons.append("Highly relevant past project experience")
        elif experience_relevance > 0.4:
            reasons.append("Some relevant project experience")
        
        if availability_score > 0.8:
            reasons.append("High availability")
        elif availability_score < 0.5:
            reasons.append("Limited availability")
        
        if performance_score > 0.7:
            reasons.append("High performance score")
        
        if cert_bonus > 0:
            reasons.append("Relevant certifications")
        
        if employee.years_of_experience >= required_exp:
            reasons.append(f"Sufficient experience ({employee.years_of_experience} years)")
        
        if not reasons:
            reasons.append("Moderate match based on overall profile")
        
        explanation = "; ".join(reasons)
        
        return total_score, explanation
    
    def find_best_matches(self, db: Session, required_skills: List[str],
                         project_category: str, project_complexity: str,
                         team_size: int, min_availability: float = 50.0,
                         department_filter: str = None) -> List[Dict]:
        """Find and rank best employee matches for a project with enhanced filtering"""
        # Build query with filters
        query = db.query(Employee).filter(
            Employee.availability_percent >= min_availability
        )
        
        # Optional department filter
        if department_filter:
            query = query.filter(Employee.department == department_filter)
        
        employees = query.all()
        
        if not employees:
            return []
        
        # Calculate match scores for all employees
        matches = []
        for employee in employees:
            score, explanation = self.calculate_match_score(
                employee, required_skills, project_category, project_complexity
            )
            
            # Get matching skills (already calculated in calculate_match_score, but we need it again for response)
            _, matching_skills, missing_skills = self.calculate_skill_match(
                required_skills, employee.skills, employee.skill_proficiency,
                employee.skill_types or []
            )
            
            # Ensure no duplicates in matching_skills
            unique_matching_skills = []
            seen = set()
            for skill in matching_skills:
                skill_lower = skill.lower()
                if skill_lower not in seen:
                    unique_matching_skills.append(skill)
                    seen.add(skill_lower)
            
            matches.append({
                'employee': employee,
                'match_score': score,
                'explanation': explanation,
                'matching_skills': unique_matching_skills,
                'missing_skills': missing_skills
            })
        
        # Sort by match score (descending)
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Return top N matches (2x team size for flexibility)
        top_matches = matches[:team_size * 2]
        
        # Format results
        results = []
        for match in top_matches:
            emp = match['employee']
            results.append({
                'employee_id': emp.id,
                'employee_name': emp.name,
                'employee_employee_id': emp.employee_id,
                'match_score': round(match['match_score'] * 100, 2),  # Convert to percentage
                'match_reason': match['explanation'],
                'skills_match': match['matching_skills'],
                'missing_skills': match['missing_skills'],
                'department': emp.department,
                'designation': emp.designation,
                'years_experience': emp.years_of_experience,
                'certifications': emp.certifications or []
            })
        
        return results
