from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class JobSearchWorker:
    def __init__(self, config: Dict):
        self.config = config
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Set up the Selenium WebDriver with Chrome."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def search_jobs(self, query: str, location: Optional[str] = None) -> List[Dict]:
        """Search for jobs using Indeed."""
        if not location:
            location = self.config.get('location', 'remote')
        
        base_url = "https://www.indeed.com"
        search_url = f"{base_url}/jobs?q={query}&l={location}"
        
        try:
            self.driver.get(search_url)
            time.sleep(2)  # Wait for dynamic content to load
            
            # Wait for job cards to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            
            # Parse the page content
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            jobs = []
            for card in job_cards[:self.config.get('max_results', 10)]:
                try:
                    title = card.find('h2', class_='jobTitle').text.strip()
                    company = card.find('span', class_='companyName').text.strip()
                    location = card.find('div', class_='companyLocation').text.strip()
                    
                    # Get job description
                    description = card.find('div', class_='job-snippet').text.strip()
                    
                    # Get job link
                    link = card.find('a', class_='jcs-JobTitle')
                    job_url = base_url + link['href'] if link else None
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'description': description,
                        'url': job_url
                    })
                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            print(f"Error searching jobs: {e}")
            return []
        
    def get_job_details(self, job_url: str) -> Optional[Dict]:
        """Get detailed information about a specific job."""
        try:
            self.driver.get(job_url)
            time.sleep(2)
            
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Extract job details
            title = soup.find('h1', class_='jobsearch-JobInfoHeader-title').text.strip()
            company = soup.find('div', class_='jobsearch-CompanyInfoContainer').text.strip()
            
            # Get full description
            description = soup.find('div', class_='jobsearch-jobDescriptionText')
            description_text = description.text.strip() if description else ""
            
            return {
                'title': title,
                'company': company,
                'description': description_text,
                'url': job_url
            }
            
        except Exception as e:
            print(f"Error getting job details: {e}")
            return None

    def __del__(self):
        """Clean up the WebDriver when the worker is destroyed."""
        if self.driver:
            self.driver.quit() 