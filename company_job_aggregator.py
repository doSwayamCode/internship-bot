"""
Company Job Aggregator
Uses publicly available job RSS feeds and APIs to find company opportunities
"""
import requests
import feedparser
from datetime import datetime
import re

class CompanyJobAggregator:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Company-specific job RSS feeds and public APIs
        self.job_sources = [
            {
                'name': 'Freshersworld',
                'url': 'https://www.freshersworld.com/jobs/rss',
                'type': 'rss'
            },
            {
                'name': 'Monster India',
                'url': 'https://www.monsterindia.com/srp/results.html?query=intern%20OR%20graduate%20OR%20trainee&geo=india',
                'type': 'html'
            }
        ]

    def scrape_freshersworld_rss(self):
        """Scrape Freshersworld RSS feed for internships"""
        jobs = []
        
        try:
            print("🔍 Checking Freshersworld RSS for new opportunities...")
            
            feed = feedparser.parse('https://www.freshersworld.com/jobs/rss')
            
            if not feed.entries:
                print("   No entries found in RSS feed")
                return jobs
            
            print(f"   Found {len(feed.entries)} total job entries")
            
            for entry in feed.entries[:20]:  # Limit to recent 20
                try:
                    title = entry.title
                    
                    # Check if it's relevant for internships/entry-level
                    if not self.is_relevant_job(title):
                        continue
                    
                    # Extract company from description if available
                    company = self.extract_company_from_description(entry.description if hasattr(entry, 'description') else "")
                    
                    if not company:
                        company = "Company not specified"
                    
                    # Check if it's from a top company
                    if self.is_top_company(company):
                        sector = self.categorize_company(company)
                        
                        job = {
                            'id': f"freshers_{hash(title + company)}_{datetime.now().strftime('%Y%m%d')}",
                            'title': title,
                            'company': company,
                            'location': self.extract_location(entry.description if hasattr(entry, 'description') else ""),
                            'sector': sector,
                            'source': 'Freshersworld RSS',
                            'link': entry.link if hasattr(entry, 'link') else "",
                            'posted_date': entry.published if hasattr(entry, 'published') else 'Recently posted',
                            'description': f"Position at {company} in {sector} sector. Check Freshersworld for detailed requirements."
                        }
                        
                        jobs.append(job)
                        
                except Exception as e:
                    print(f"   ⚠️ Error processing entry: {e}")
                    continue
            
            print(f"✅ Freshersworld: Found {len(jobs)} relevant company positions")
            
        except Exception as e:
            print(f"❌ Error scraping Freshersworld RSS: {e}")
        
        return jobs

    def generate_mock_company_jobs(self):
        """Generate mock company job listings for demonstration"""
        print("🏢 Generating sample company job opportunities...")
        
        # Mock data for top companies (this would be replaced with real API calls)
        mock_jobs = [
            {
                'id': f"company_mock_{datetime.now().strftime('%Y%m%d')}_1",
                'title': 'Software Development Intern',
                'company': 'Microsoft India',
                'location': 'Hyderabad, India',
                'sector': 'Technology',
                'source': 'Company Portal',
                'link': 'https://careers.microsoft.com/students',
                'posted_date': 'Recently posted',
                'description': 'Software development internship at Microsoft India. Work on cutting-edge technology with experienced mentors.'
            },
            {
                'id': f"company_mock_{datetime.now().strftime('%Y%m%d')}_2",
                'title': 'Data Science Graduate Trainee',
                'company': 'Amazon India',
                'location': 'Bangalore, India', 
                'sector': 'Technology',
                'source': 'Company Portal',
                'link': 'https://amazon.jobs/en/teams/university-programs',
                'posted_date': 'Recently posted',
                'description': 'Graduate trainee program in data science at Amazon India. 12-month rotation program.'
            },
            {
                'id': f"company_mock_{datetime.now().strftime('%Y%m%d')}_3",
                'title': 'Management Trainee Program',
                'company': 'Tata Motors',
                'location': 'Pune, India',
                'sector': 'Automotive',
                'source': 'Company Portal', 
                'link': 'https://careers.tatamotors.com',
                'posted_date': 'Recently posted',
                'description': 'Management trainee program at Tata Motors. Exposure to various business functions in automotive industry.'
            },
            {
                'id': f"company_mock_{datetime.now().strftime('%Y%m%d')}_4",
                'title': 'Finance Graduate Associate',
                'company': 'HDFC Bank',
                'location': 'Mumbai, India',
                'sector': 'Banking/Finance',
                'source': 'Company Portal',
                'link': 'https://www.hdfcbank.com/personal/about-us/careers',
                'posted_date': 'Recently posted',
                'description': 'Graduate associate program in finance at HDFC Bank. Training in banking operations and financial services.'
            },
            {
                'id': f"company_mock_{datetime.now().strftime('%Y%m%d')}_5",
                'title': 'Marketing Intern',
                'company': 'Unilever India',
                'location': 'Mumbai, India',
                'sector': 'FMCG',
                'source': 'Company Portal',
                'link': 'https://careers.unilever.com',
                'posted_date': 'Recently posted',
                'description': 'Marketing internship at Unilever India. Work on brand management and consumer insights projects.'
            },
            {
                'id': f"company_mock_{datetime.now().strftime('%Y%m%d')}_6",
                'title': 'Engineering Graduate Trainee',
                'company': 'Larsen & Toubro',
                'location': 'Chennai, India',
                'sector': 'Engineering/Construction',
                'source': 'Company Portal',
                'link': 'https://careers.larsentoubro.com',
                'posted_date': 'Recently posted',
                'description': 'Graduate trainee program for engineers at L&T. Exposure to infrastructure and engineering projects.'
            }
        ]
        
        print(f"✅ Generated {len(mock_jobs)} sample company opportunities")
        return mock_jobs

    def extract_company_from_description(self, description):
        """Extract company name from job description"""
        # Simple extraction - look for common patterns
        patterns = [
            r'at\s+([A-Z][a-zA-Z\s&]+?)(?:\s+is\s|\s+in\s|\.|,)',
            r'Company:\s*([A-Z][a-zA-Z\s&]+?)(?:\n|,|\.)',
            r'([A-Z][a-zA-Z\s&]+?)\s+is\s+hiring'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description)
            if match:
                return match.group(1).strip()
        
        return None

    def extract_location(self, description):
        """Extract location from description"""
        # Look for common Indian city patterns
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Gurgaon', 'Noida']
        
        for city in cities:
            if city.lower() in description.lower():
                return f"{city}, India"
        
        return "India"

    def is_top_company(self, company):
        """Check if company is a top/well-known company"""
        top_companies = [
            'microsoft', 'google', 'amazon', 'meta', 'facebook', 'apple', 'adobe', 'netflix',
            'tata', 'infosys', 'tcs', 'wipro', 'hcl', 'cognizant', 'accenture',
            'hdfc', 'icici', 'sbi', 'axis', 'kotak',
            'unilever', 'nestle', 'itc', 'pepsico', 'coca cola',
            'mahindra', 'bajaj', 'maruti', 'hyundai',
            'deloitte', 'pwc', 'kpmg', 'ernst', 'young'
        ]
        
        company_lower = company.lower()
        return any(top_company in company_lower for top_company in top_companies)

    def categorize_company(self, company):
        """Categorize company by sector"""
        company_lower = company.lower()
        
        if any(tech in company_lower for tech in ['microsoft', 'google', 'amazon', 'meta', 'facebook', 'adobe', 'infosys', 'tcs', 'wipro', 'hcl', 'tech']):
            return 'Technology'
        elif any(bank in company_lower for bank in ['bank', 'hdfc', 'icici', 'sbi', 'axis', 'kotak', 'finance']):
            return 'Banking/Finance'
        elif any(auto in company_lower for auto in ['tata motors', 'mahindra', 'bajaj', 'maruti', 'hyundai', 'auto']):
            return 'Automotive'
        elif any(fmcg in company_lower for fmcg in ['unilever', 'nestle', 'itc', 'pepsico', 'coca cola']):
            return 'FMCG'
        elif any(consult in company_lower for consult in ['deloitte', 'pwc', 'kpmg', 'ernst', 'young', 'accenture']):
            return 'Consulting'
        else:
            return 'General'

    def is_relevant_job(self, title):
        """Check if job is relevant for internships/entry-level"""
        if not title:
            return False
            
        title_lower = title.lower()
        
        relevant_keywords = [
            'intern', 'internship', 'graduate', 'trainee', 'entry level', 'junior',
            'fresher', 'associate', 'apprentice', 'campus', 'new grad'
        ]
        
        exclude_keywords = [
            'senior', 'lead', 'manager', 'director', 'head', 'chief', 'principal',
            'experienced', '5+ years', '3+ years'
        ]
        
        # Check exclusions first
        for keyword in exclude_keywords:
            if keyword in title_lower:
                return False
        
        # Check relevant keywords
        for keyword in relevant_keywords:
            if keyword in title_lower:
                return True
        
        return False

    def scrape_all_company_opportunities(self):
        """Main method to scrape all company opportunities"""
        all_jobs = []
        
        print("🏢 Starting company-specific opportunity search...")
        
        # Try RSS feeds
        try:
            rss_jobs = self.scrape_freshersworld_rss()
            all_jobs.extend(rss_jobs)
        except Exception as e:
            print(f"⚠️ RSS scraping failed: {e}")
        
        # Add mock data for demonstration (replace with real APIs when available)
        mock_jobs = self.generate_mock_company_jobs()
        all_jobs.extend(mock_jobs)
        
        # Remove duplicates
        unique_jobs = []
        seen_combinations = set()
        
        for job in all_jobs:
            combination = (job['title'].lower(), job['company'].lower())
            if combination not in seen_combinations:
                unique_jobs.append(job)
                seen_combinations.add(combination)
        
        # Summary
        print(f"\n📊 COMPANY OPPORTUNITIES SUMMARY:")
        print(f"Total positions found: {len(unique_jobs)}")
        
        sectors = {}
        for job in unique_jobs:
            sector = job['sector']
            sectors[sector] = sectors.get(sector, 0) + 1
        
        for sector, count in sectors.items():
            print(f"  {sector}: {count} positions")
        
        return unique_jobs

def scrape_company_careers():
    """Main function to get company career opportunities"""
    aggregator = CompanyJobAggregator()
    return aggregator.scrape_all_company_opportunities()

if __name__ == "__main__":
    jobs = scrape_company_careers()
    print(f"\n✅ Found {len(jobs)} total company opportunities!")
    
    if jobs:
        print("\n📋 Sample Results:")
        for i, job in enumerate(jobs[:5]):
            print(f"{i+1}. {job['title']} at {job['company']} ({job['sector']}) - {job['source']}")
