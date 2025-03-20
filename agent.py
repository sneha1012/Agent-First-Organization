from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JobAnalysis(BaseModel):
    """Schema for job analysis output."""
    required_skills: List[str] = Field(description="List of required skills for the job")
    experience_level: str = Field(description="Required experience level (e.g., 'Entry Level', 'Mid Level', 'Senior')")
    salary_range: Optional[str] = Field(description="Estimated salary range if available")
    company_culture: Optional[str] = Field(description="Inferred company culture based on the job posting")
    growth_potential: str = Field(description="Assessment of growth potential in this role")

class JobAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.llm = ChatOpenAI(
            model=config.get('model', 'gpt-4'),
            temperature=config.get('temperature', 0.7),
            max_tokens=config.get('max_tokens', 1000)
        )
        self.parser = PydanticOutputParser(pydantic_object=JobAnalysis)

    def analyze_job(self, job_details: Dict) -> JobAnalysis:
        """Analyze a job posting and extract key information."""
        template = """You are an expert job analyst. Analyze the following job posting and provide a structured analysis.
        
        Job Title: {title}
        Company: {company}
        Description: {description}
        
        Please analyze this job posting and provide:
        1. Required skills
        2. Experience level
        3. Salary range (if mentioned)
        4. Company culture (based on the posting)
        5. Growth potential assessment
        
        {format_instructions}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        messages = prompt.format_messages(
            title=job_details['title'],
            company=job_details['company'],
            description=job_details['description'],
            format_instructions=self.parser.get_format_instructions()
        )
        
        response = self.llm.invoke(messages)
        return self.parser.parse(response.content)

    def prepare_application(self, job_details: Dict, analysis: JobAnalysis) -> Dict:
        """Prepare application materials based on job details and analysis."""
        template = """You are an expert job application consultant. Based on the job posting and analysis, prepare application materials.
        
        Job Details:
        Title: {title}
        Company: {company}
        Description: {description}
        
        Analysis:
        Required Skills: {skills}
        Experience Level: {experience}
        Company Culture: {culture}
        
        Please provide:
        1. A tailored cover letter
        2. Key points to highlight in the resume
        3. Suggested interview preparation topics
        
        Format your response as a JSON object with the following keys:
        - cover_letter: The complete cover letter text
        - resume_highlights: List of key points to emphasize
        - interview_prep: List of topics to prepare for
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        messages = prompt.format_messages(
            title=job_details['title'],
            company=job_details['company'],
            description=job_details['description'],
            skills=", ".join(analysis.required_skills),
            experience=analysis.experience_level,
            culture=analysis.company_culture or "Not specified"
        )
        
        response = self.llm.invoke(messages)
        return response.content

    def filter_jobs(self, jobs: List[Dict], criteria: Dict) -> List[Dict]:
        """Filter jobs based on user criteria using AI analysis."""
        template = """You are an expert job matcher. Analyze the following job and determine if it matches the user's criteria.
        
        Job:
        Title: {title}
        Company: {company}
        Description: {description}
        
        User Criteria:
        {criteria}
        
        Please analyze if this job matches the user's criteria and provide a score from 0-100.
        Return a JSON object with:
        - matches: boolean
        - score: number
        - reasoning: string
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        matching_jobs = []
        
        for job in jobs:
            messages = prompt.format_messages(
                title=job['title'],
                company=job['company'],
                description=job['description'],
                criteria=str(criteria)
            )
            
            response = self.llm.invoke(messages)
            result = response.content
            
            if result.get('matches', False):
                job['match_score'] = result.get('score', 0)
                job['match_reasoning'] = result.get('reasoning', '')
                matching_jobs.append(job)
        
        # Sort by match score
        matching_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        return matching_jobs 