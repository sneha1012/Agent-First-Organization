import json
from typing import Dict, List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from worker import JobSearchWorker
from agent import JobAgent
from resume_parser import ResumeParserWorker
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="AIHawk Job Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobAssistant:
    def __init__(self, config_path: str = "config.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize workers and agents
        self.job_worker = JobSearchWorker(self.config['workers']['job_search']['config'])
        self.resume_worker = ResumeParserWorker(self.config['workers']['resume_parser']['config'])
        self.job_agent = JobAgent(self.config['agents']['job_agent']['config'])

    def search_jobs(self, query: str, location: str = None, criteria: Dict = None) -> List[Dict]:
        """Search for jobs and filter based on criteria."""
        jobs = self.job_worker.search_jobs(query, location)
        if criteria:
            jobs = self.job_agent.filter_jobs(jobs, criteria)
        return jobs

    def analyze_job(self, job_url: str) -> Dict:
        """Get detailed analysis of a specific job."""
        job_details = self.job_worker.get_job_details(job_url)
        if not job_details:
            return {"error": "Failed to fetch job details"}
        
        analysis = self.job_agent.analyze_job(job_details)
        application = self.job_agent.prepare_application(job_details, analysis)
        
        return {
            "job_details": job_details,
            "analysis": analysis.dict(),
            "application": application
        }

    def analyze_resume(self, resume_text: str) -> Dict:
        """Analyze resume text."""
        analysis = self.resume_worker.parse_resume(resume_text)
        return analysis.dict()

    def match_resume_job(self, resume_text: str, job_url: str) -> Dict:
        """Match resume with job requirements."""
        job_details = self.job_worker.get_job_details(job_url)
        if not job_details:
            return {"error": "Failed to fetch job details"}
        
        resume_analysis = self.resume_worker.parse_resume(resume_text)
        match_result = self.resume_worker.match_job_requirements(resume_analysis, job_details)
        improvements = self.resume_worker.suggest_improvements(resume_analysis, job_details)
        
        return {
            "match_result": match_result,
            "improvements": improvements
        }

# Initialize the job assistant
assistant = JobAssistant()

@app.post("/api/search-jobs")
async def search_jobs(query: str, location: Optional[str] = None):
    """Search for jobs based on query and location."""
    try:
        jobs = assistant.search_jobs(query, location)
        return JSONResponse(content={"jobs": jobs})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-job")
async def analyze_job(job_url: str):
    """Analyze a specific job posting."""
    try:
        result = assistant.analyze_job(job_url)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-resume")
async def analyze_resume(resume_text: str):
    """Analyze resume text."""
    try:
        result = assistant.analyze_resume(resume_text)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match-resume-job")
async def match_resume_job(resume_text: str, job_url: str):
    """Match resume with job requirements."""
    try:
        result = assistant.match_resume_job(resume_text, job_url)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to AIHawk Job Assistant API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=assistant.config['api']['host'],
        port=assistant.config['api']['port'],
        reload=assistant.config['api']['debug']
    ) 