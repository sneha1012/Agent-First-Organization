from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResumeAnalysis(BaseModel):
    """Schema for resume analysis output."""
    skills: List[str] = Field(description="List of skills found in the resume")
    experience: List[Dict] = Field(description="List of work experiences with details")
    education: List[Dict] = Field(description="List of educational qualifications")
    certifications: List[str] = Field(description="List of certifications")
    summary: str = Field(description="Professional summary of the candidate")

class ResumeParserWorker:
    def __init__(self, config: Dict):
        self.config = config
        self.llm = ChatOpenAI(
            model=config.get('model', 'gpt-4'),
            max_tokens=config.get('max_tokens', 2000)
        )
        self.parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)

    def parse_resume(self, resume_text: str) -> ResumeAnalysis:
        """Parse and analyze resume text."""
        template = """You are an expert resume parser. Analyze the following resume text and extract key information.
        
        Resume Text:
        {resume_text}
        
        Please analyze this resume and provide:
        1. List of skills
        2. Work experience with details
        3. Educational qualifications
        4. Certifications
        5. Professional summary
        
        {format_instructions}
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        messages = prompt.format_messages(
            resume_text=resume_text,
            format_instructions=self.parser.get_format_instructions()
        )
        
        response = self.llm.invoke(messages)
        return self.parser.parse(response.content)

    def match_job_requirements(self, resume_analysis: ResumeAnalysis, job_requirements: Dict) -> Dict:
        """Match resume with job requirements."""
        template = """You are an expert job matcher. Analyze how well the candidate's resume matches the job requirements.
        
        Resume Analysis:
        Skills: {skills}
        Experience: {experience}
        Education: {education}
        
        Job Requirements:
        {requirements}
        
        Please provide:
        1. Match score (0-100)
        2. Matching skills
        3. Missing skills
        4. Experience match
        5. Detailed analysis
        
        Format your response as a JSON object with the following keys:
        - match_score: number
        - matching_skills: list of strings
        - missing_skills: list of strings
        - experience_match: string
        - analysis: string
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        messages = prompt.format_messages(
            skills=", ".join(resume_analysis.skills),
            experience=str(resume_analysis.experience),
            education=str(resume_analysis.education),
            requirements=str(job_requirements)
        )
        
        response = self.llm.invoke(messages)
        return response.content

    def suggest_improvements(self, resume_analysis: ResumeAnalysis, job_requirements: Dict) -> Dict:
        """Suggest improvements to better match job requirements."""
        template = """You are an expert resume consultant. Analyze the resume against job requirements and suggest improvements.
        
        Resume Analysis:
        Skills: {skills}
        Experience: {experience}
        Education: {education}
        
        Job Requirements:
        {requirements}
        
        Please provide:
        1. Skills to develop
        2. Experience to highlight
        3. Keywords to include
        4. Format suggestions
        5. Action items
        
        Format your response as a JSON object with the following keys:
        - skills_to_develop: list of strings
        - experience_to_highlight: list of strings
        - keywords: list of strings
        - format_suggestions: list of strings
        - action_items: list of strings
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        messages = prompt.format_messages(
            skills=", ".join(resume_analysis.skills),
            experience=str(resume_analysis.experience),
            education=str(resume_analysis.education),
            requirements=str(job_requirements)
        )
        
        response = self.llm.invoke(messages)
        return response.content 