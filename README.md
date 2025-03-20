# AIHawk Job Assistant - Arklex Framework Implementation

This project implements a job application assistant using the Arklex framework, following the screening test requirements. The assistant helps users search for jobs, analyze job postings, and prepare application materials using AI-powered analysis.

## Project Structure

```
.
├── main.py           # FastAPI server and main application logic
├── worker.py         # Job search worker implementation
├── agent.py          # Job analysis agent implementation
├── resume_parser.py  # Resume parsing and analysis
├── config.json       # Application configuration
├── requirements.txt  # Project dependencies
└── README.md        # This file
```

## Features Implemented

1. **Arklex Framework Integration**
   - Workers for task execution
   - Agents for decision making
   - Task graph structure

2. **Job Search and Analysis**
   - Indeed job scraping
   - Job requirement analysis
   - Company culture analysis
   - Growth potential assessment

3. **Resume Analysis**
   - Skills extraction
   - Experience analysis
   - Education parsing
   - Certification identification

4. **Job-Resume Matching**
   - Requirement matching
   - Skills gap analysis
   - Experience alignment
   - Improvement suggestions

5. **API Interface**
   - RESTful endpoints
   - FastAPI implementation
   - Swagger documentation

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     MODEL_NAME=gpt-4
     MAX_TOKENS=2000
     TEMPERATURE=0.7
     ```

4. Run the application:
```bash
python main.py
```

5. Access the API:
   - Open http://localhost:8000/docs in your browser
   - Use the Swagger UI to test endpoints

## API Endpoints

1. **Search Jobs**
   ```bash
   POST /api/search-jobs
   Query Parameters:
   - query: Job search query
   - location: Job location (optional)
   ```

2. **Analyze Job**
   ```bash
   POST /api/analyze-job
   Query Parameters:
   - job_url: Indeed job posting URL
   ```

3. **Analyze Resume**
   ```bash
   POST /api/analyze-resume
   Body:
   {
     "resume_text": "Your resume text here..."
   }
   ```

4. **Match Resume with Job**
   ```bash
   POST /api/match-resume-job
   Body:
   {
     "resume_text": "Your resume text...",
     "job_url": "https://www.indeed.com/..."
   }
   ```

## Implementation Details

1. **Workers**
   - `JobSearchWorker`: Handles job search and scraping
   - `ResumeParserWorker`: Processes resume analysis

2. **Agents**
   - `JobAgent`: Analyzes jobs and prepares applications
   - `ResumeAgent`: Processes resume information

3. **Task Graph**
   - Job Search → Analysis → Application Preparation
   - Resume Analysis → Job Matching → Improvement Suggestions

## Testing

1. Start the server:
```bash
python main.py
```

2. Test endpoints using curl:
```bash
# Test job search
curl -X POST "http://localhost:8000/api/search-jobs?query=software+engineer&location=remote"

# Test job analysis
curl -X POST "http://localhost:8000/api/analyze-job?job_url=https://www.indeed.com/..."

# Test resume analysis
curl -X POST "http://localhost:8000/api/analyze-resume" \
     -H "Content-Type: application/json" \
     -d '{"resume_text": "Your resume text here..."}'
```

## Notes

- The application uses GPT-4 for AI-powered analysis
- Job search is implemented using Indeed
- All API responses are in JSON format
- Error handling is implemented for all endpoints

## License

MIT License - see LICENSE file for details