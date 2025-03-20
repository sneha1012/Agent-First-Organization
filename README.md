# JobSearchPro

An intelligent job application assistant built using the Arklex framework, designed to help job seekers find, analyze, and apply for jobs more effectively.

## 🚀 Features

- **Smart Job Search**: Intelligent job search across multiple platforms with customizable filters
- **Job Analysis**: Deep analysis of job postings using AI to extract key requirements and opportunities
- **Resume Matching**: AI-powered resume analysis and matching with job requirements
- **Application Preparation**: Automated generation of tailored cover letters and application materials
- **Interactive API**: RESTful API endpoints for seamless integration with other applications

## 🛠️ Technology Stack

- **Framework**: Arklex Agent First Organization
- **AI Models**: GPT-4 for natural language processing and analysis
- **Web Scraping**: Selenium for job data collection
- **API**: FastAPI for RESTful endpoints
- **Database**: In-memory storage for job and resume data
- **Frontend**: Swagger UI for API documentation and testing

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Chrome browser (for web scraping)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/JobSearchPro.git
cd JobSearchPro
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## 🚀 Usage

1. Start the server:
```bash
python main.py
```

2. Access the API documentation:
Open your browser and navigate to `http://localhost:8000/docs`

3. Available Endpoints:

- `POST /api/search-jobs`: Search for jobs based on query and location
- `POST /api/analyze-job`: Analyze a specific job posting
- `POST /api/analyze-resume`: Analyze resume text
- `POST /api/match-resume-job`: Match resume with job requirements

## 🏗️ Project Structure

```
JobSearchPro/
├── main.py              # FastAPI application and endpoints
├── worker.py            # Job search and web scraping worker
├── agent.py             # AI agent for job analysis
├── resume_parser.py     # Resume parsing and analysis
├── config.json          # Application configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## 🤖 AI Capabilities

The assistant leverages advanced AI models to provide:

1. **Job Analysis**:
   - Extracts key requirements and qualifications
   - Identifies company culture and values
   - Analyzes growth potential and opportunities

2. **Resume Matching**:
   - Parses and analyzes resume content
   - Matches skills and experience with job requirements
   - Provides improvement suggestions

3. **Application Preparation**:
   - Generates tailored cover letters
   - Highlights relevant experience
   - Optimizes application materials

## 🔍 Example Usage

```python
# Search for jobs
response = requests.post(
    "http://localhost:8000/api/search-jobs",
    json={"query": "software engineer", "location": "remote"}
)

# Analyze a job posting
response = requests.post(
    "http://localhost:8000/api/analyze-job",
    json={"job_url": "https://example.com/job-posting"}
)

# Match resume with job
response = requests.post(
    "http://localhost:8000/api/match-resume-job",
    json={
        "resume_text": "Your resume content here",
        "job_url": "https://example.com/job-posting"
    }
)
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🙏 Acknowledgments

- Built with the [Arklex](https://github.com/arklex-ai/arklex) framework
- Powered by OpenAI's GPT-4 model
- Inspired by the need for smarter job application processes