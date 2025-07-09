from bs4 import BeautifulSoup
import requests
import re
import time
import json
from urllib.parse import urljoin, quote

# Comprehensive keywords for filtering (based on your requirements)
TECH_KEYWORDS = [
    # Software Engineering
    'software engineer', 'software developer', 'programming', 'coding', 'python', 'java', 
    'javascript', 'react', 'node', 'web development', 'app development', 'mobile app', 
    'android', 'ios', 'flutter', 'backend', 'frontend', 'fullstack', 'devops', 'cloud', 
    'aws', 'database', 'sql', 'mongodb', 'api', 'tech', 'technology', 'IT', 'computer science',
    'cybersecurity', 'blockchain', 'qa', 'testing', 'automation', 'selenium', 'framework', 
    'git', 'docker', 'kubernetes', 'microservices', 'rest api', 'graphql',
    
    # AI/ML & Data Analytics
    'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
    'data science', 'data analyst', 'data analytics', 'big data', 'statistics', 
    'predictive analytics', 'business intelligence', 'tableau', 'power bi', 'excel',
    'r programming', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
    'nlp', 'computer vision', 'opencv', 'keras', 'jupyter', 'spark', 'hadoop',
    
    # UI/UX Design
    'ui/ux', 'ui designer', 'ux designer', 'user interface', 'user experience',
    'graphic design', 'web design', 'figma', 'adobe', 'sketch', 'wireframe',
    'prototype', 'user research', 'usability', 'interaction design',
    
    # Business Development
    'business development', 'business analyst', 'business intelligence', 'strategy',
    'market research', 'sales', 'marketing', 'product management', 'product manager',
    'digital marketing', 'social media', 'content marketing', 'growth hacking',
    
    # Non-Tech Specialized Roles
    'esg', 'environmental social governance', 'sustainability', 'ccass', 'compliance',
    'environment engineer', 'environmental engineering', 'climate', 'carbon',
    'renewable energy', 'green technology', 'corporate social responsibility',
    'risk management', 'audit', 'finance', 'consulting', 'research', 'policy'
]

def is_tech_related(title, company=""):
    """Check if internship is tech-related based on title and company"""
    text_to_check = f"{title} {company}".lower()
    
    for keyword in TECH_KEYWORDS:
        if keyword.lower() in text_to_check:
            return True
    return False

def scrape_internshala():
    """Scrape tech internships from Internshala"""
    print("Scraping Internshala...")
    
    # Search for specific categories on Internshala
    tech_urls = [
        "https://internshala.com/internships/computer-science",
        "https://internshala.com/internships/web-development", 
        "https://internshala.com/internships/software-development",
        "https://internshala.com/internships/data-science",
        "https://internshala.com/internships/android-app-development",
        "https://internshala.com/internships/python",
        "https://internshala.com/internships/machine-learning",
        "https://internshala.com/internships/artificial-intelligence",
        "https://internshala.com/internships/ui-ux-design",
        "https://internshala.com/internships/business-development",
        "https://internshala.com/internships"  # General search as fallback
    ]
    
    results = []
    
    for url in tech_urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            listings = soup.select(".individual_internship")[:10]  # Get more listings
            
            for listing in listings:
                # Get title using correct selector
                title_tag = listing.select_one(".job-title-href")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)

                # Company name selector
                company_tag = listing.select_one(".company-name")
                company = company_tag.get_text(strip=True) if company_tag else "Unknown Company"

                # Only include relevant internships
                if not is_tech_related(title, company):
                    continue

                # Link
                link_tag = listing.select_one("a")
                link = "https://internshala.com" + link_tag['href'] if link_tag else "#"

                # Extract dates
                posted_date = "Not specified"
                deadline = "Not specified"
                
                try:
                    # Get all text from the listing for pattern matching
                    listing_text = listing.get_text()
                    
                    # Look for Internshala-specific date patterns
                    import re
                    
                    # Pattern for "X days ago", "X weeks ago", "X months ago"
                    posted_pattern = re.search(r'(\d+\s+(?:day|week|month)s?\s+ago)', listing_text, re.IGNORECASE)
                    if posted_pattern:
                        posted_date = posted_pattern.group(1)
                    
                    # Pattern for "Apply by" or "Last date" with dates
                    deadline_pattern = re.search(r'(?:apply\s+by|last\s+date|deadline)[:\s]*([^a-z]*(?:\d{1,2}[^\w]*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|\d{1,2}[/-]\d{1,2}[/-]?\d{0,4}))', listing_text, re.IGNORECASE)
                    if deadline_pattern:
                        deadline = deadline_pattern.group(1).strip()
                    
                    # Alternative: look for specific selectors
                    date_elements = listing.select(".date, .posted_date, .apply_by, .deadline, .posted-date")
                    for date_elem in date_elements:
                        date_text = date_elem.get_text(strip=True)
                        if 'ago' in date_text.lower():
                            posted_date = date_text
                        elif any(word in date_text.lower() for word in ['apply by', 'deadline', 'last date']):
                            deadline = date_text
                    
                except Exception as e:
                    pass

                # Unique job ID (using last part of URL)
                job_id = link.split('/')[-1]

                internship_data = {
                    "id": "internshala_" + job_id,
                    "title": title,
                    "company": company,
                    "link": link,
                    "source": "Internshala",
                    "posted_date": posted_date,
                    "deadline": deadline
                }
                
                # Avoid duplicates
                if not any(existing['id'] == internship_data['id'] for existing in results):
                    results.append(internship_data)
                    print(f"✅ Found: {title} at {company}")
                    
        except Exception as e:
            print(f"⚠️ Error scraping {url}: {e}")
            continue
            
        # Limit total results to avoid overwhelming
        if len(results) >= 20:
            break

    print(f"� Internshala: Found {len(results)} internships")
    return results


def scrape_naukri():
    """Scrape internships from Naukri.com - Improved version"""
    print("Scraping Naukri...")
    
    results = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        # Use more specific Naukri search URLs
        base_searches = [
            "software+developer+internship",
            "data+science+internship", 
            "python+internship",
            "machine+learning+internship",
            "business+development+internship",
            "ui+ux+internship"
        ]
        
        for search_term in base_searches:
            try:
                # Use Naukri's search API endpoint format
                url = f"https://www.naukri.com/internship-jobs?k={search_term}&l=India"
                print(f"   Checking: {search_term}")
                
                session = requests.Session()
                session.headers.update(headers)
                
                response = session.get(url, timeout=15)
                
                if response.status_code != 200:
                    print(f"   Status code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try multiple selectors for Naukri listings (they change frequently)
                selectors_to_try = [
                    ".srp-jobtuple-wrapper",
                    ".jobTuple",
                    ".jobTupleHeader", 
                    "[data-job-id]",
                    ".row1",
                    ".jobTupleWrap",
                    ".list",
                    ".job-summary"
                ]
                
                listings = []
                for selector in selectors_to_try:
                    listings = soup.select(selector)
                    if listings:
                        print(f"   Found {len(listings)} listings with selector: {selector}")
                        break
                
                # If no job listings found, try extracting from script tags (JSON data)
                if not listings:
                    script_tags = soup.find_all('script', type='application/ld+json')
                    for script in script_tags:
                        try:
                            data = json.loads(script.string)
                            if isinstance(data, dict) and 'jobPosting' in str(data).lower():
                                # Extract job data from JSON-LD
                                if 'title' in data and 'hiringOrganization' in data:
                                    title = data.get('title', '')
                                    company = data.get('hiringOrganization', {}).get('name', 'Unknown')
                                    
                                    if is_tech_related(title, company) or 'intern' in title.lower():
                                        job_id = abs(hash(title + company + "naukri")) % 1000000
                                        results.append({
                                            "id": f"naukri_{job_id}",
                                            "title": title,
                                            "company": company,
                                            "link": data.get('url', url),
                                            "source": "Naukri"
                                        })
                                        print(f"✅ Found (JSON): {title} at {company}")
                        except:
                            continue
                
                # Process HTML listings
                for listing in listings[:10]:
                    try:
                        # Try multiple approaches to extract title
                        title = None
                        title_selectors = [
                            ".title a",
                            ".jobTupleHeader .title a",
                            "h3 a",
                            "h2 a",
                            "[data-job-title]",
                            ".job-title",
                            "a[title]"
                        ]
                        
                        for selector in title_selectors:
                            title_elem = listing.select_one(selector)
                            if title_elem:
                                title = title_elem.get_text(strip=True) or title_elem.get('title', '').strip()
                                if title and len(title) > 5:
                                    break
                        
                        if not title:
                            continue
                        
                        # Extract company
                        company = None
                        company_selectors = [
                            ".subTitle a",
                            ".companyName",
                            ".comp-name",
                            "[data-company]",
                            ".company"
                        ]
                        
                        for selector in company_selectors:
                            company_elem = listing.select_one(selector)
                            if company_elem:
                                company = company_elem.get_text(strip=True)
                                if company:
                                    break
                        
                        company = company or "Company Name Not Listed"
                        
                        # Check relevance
                        if not (is_tech_related(title, company) or 'intern' in title.lower()):
                            continue
                        
                        # Extract link
                        link_elem = listing.select_one("a") or listing.select_one(".title a")
                        link = link_elem.get('href', '#') if link_elem else '#'
                        
                        if link.startswith('/'):
                            link = "https://www.naukri.com" + link
                        elif not link.startswith('http'):
                            link = f"https://www.naukri.com/job-listings-{abs(hash(title + company)) % 100000}"
                        
                        job_id = abs(hash(title + company + "naukri")) % 1000000
                        
                        internship_data = {
                            "id": f"naukri_{job_id}",
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "Naukri",
                            "posted_date": "Not specified",
                            "deadline": "Not specified"
                        }
                        
                        if not any(existing['id'] == internship_data['id'] for existing in results):
                            results.append(internship_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        continue
                
                time.sleep(1)  # Be respectful to the server
                        
            except Exception as e:
                print(f"⚠️ Error with search term {search_term}: {e}")
                continue
                
            if len(results) >= 10:
                break
        
        # Alternative approach: Use direct category URLs and different search methods
        if len(results) < 3:
            try:
                # Try job aggregator sites that list Naukri jobs
                alternative_sources = [
                    "https://www.foundit.in/seeker/search/jobs?query=internship&locations=India",
                    "https://www.careerpower.in/internship-jobs.html"
                ]
                
                for alt_url in alternative_sources:
                    try:
                        response = requests.get(alt_url, headers=headers, timeout=15)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for any internship links
                        all_links = soup.find_all('a', href=True)
                        for link in all_links[:15]:
                            text = link.get_text(strip=True)
                            href = link.get('href', '')
                            
                            if (len(text) > 10 and 
                                ('intern' in text.lower() or is_tech_related(text)) and
                                ('job' in href or 'internship' in href)):
                                
                                job_id = abs(hash(text + "naukri_alt")) % 1000000
                                
                                if not any(existing['id'] == f"naukri_{job_id}" for existing in results):
                                    results.append({
                                        "id": f"naukri_{job_id}",
                                        "title": text,
                                        "company": "Various Companies",
                                        "link": urljoin(alt_url, href),
                                        "source": "Naukri/Alternative",
                                        "posted_date": "Not specified",
                                        "deadline": "Not specified"
                                    })
                                    print(f"✅ Found (alternative): {text}")
                                    
                                    if len(results) >= 3:
                                        break
                        
                        if len(results) >= 3:
                            break
                            
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"⚠️ Naukri alternative approach failed: {e}")
        
        # Final fallback: Create sample listings if no results found
        if len(results) == 0:
            print("   ℹ️ No direct results found - Naukri may have anti-bot protection")
            # Don't create fake results, just acknowledge the limitation
                
    except Exception as e:
        print(f"⚠️ Error scraping Naukri: {e}")
    
    print(f"📦 Naukri: Found {len(results)} internships")
    return results


def scrape_unstop():
    """Scrape internships from Unstop (formerly Dare2Compete) - Improved version"""
    print("🔍 Scraping Unstop...")
    
    results = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        }
        
        # Unstop URLs with better targeting
        unstop_urls = [
            "https://unstop.com/jobs?opportunity_type=internship",
            "https://unstop.com/internships?opportunity_type=internship",
            "https://unstop.com/opportunities?opportunity_type=internship&job_category=engineering",
            "https://unstop.com/opportunities?opportunity_type=internship&job_category=computer-science",
            "https://unstop.com/opportunities?search=software%20engineer%20internship",
            "https://unstop.com/opportunities?search=data%20science%20internship"
        ]
        
        for url in unstop_urls:
            try:
                print(f"   Checking: {url}")
                
                session = requests.Session()
                session.headers.update(headers)
                
                response = session.get(url, timeout=15)
                
                if response.status_code != 200:
                    print(f"   Status code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try multiple selectors for Unstop listings
                selectors_to_try = [
                    "[data-testid='opportunity-card']",
                    ".opportunity-card",
                    ".job-card",
                    ".card",
                    ".listing-card",
                    "[class*='opportunity']",
                    "[class*='internship']",
                    "article",
                    ".opportunityCard",
                    ".opp-card"
                ]
                
                listings = []
                for selector in selectors_to_try:
                    listings = soup.select(selector)
                    if listings:
                        print(f"   Found {len(listings)} listings with selector: {selector}")
                        break
                
                # Alternative: Look for JSON data in script tags
                if not listings:
                    scripts = soup.find_all('script', type='application/json')
                    for script in scripts:
                        try:
                            data = json.loads(script.string)
                            if isinstance(data, dict) and 'opportunities' in str(data).lower():
                                # Extract from JSON if available
                                pass  # Implement if needed
                        except:
                            continue
                
                for listing in listings[:12]:
                    try:
                        # Extract title with multiple approaches
                        title = None
                        title_selectors = [
                            "[data-testid='opportunity-title']",
                            ".opportunity-title",
                            ".job-title",
                            ".title",
                            "h3",
                            "h2", 
                            "h4",
                            "a[title]",
                            ".card-title",
                            "[class*='title']"
                        ]
                        
                        for selector in title_selectors:
                            title_elem = listing.select_one(selector)
                            if title_elem:
                                title = title_elem.get_text(strip=True) or title_elem.get('title', '').strip()
                                if title and len(title) > 5:
                                    break
                        
                        if not title:
                            continue
                        
                        # Extract company
                        company = None
                        company_selectors = [
                            "[data-testid='company-name']",
                            ".company-name",
                            ".company",
                            ".organization",
                            "[class*='company']",
                            "[class*='org']",
                            ".brand",
                            ".organizer"
                        ]
                        
                        for selector in company_selectors:
                            company_elem = listing.select_one(selector)
                            if company_elem:
                                company = company_elem.get_text(strip=True)
                                if company:
                                    break
                        
                        company = company or "Company Name Not Listed"
                        
                        # Check relevance
                        if not (is_tech_related(title, company) or 'intern' in title.lower()):
                            continue
                        
                        # Extract link
                        link_elem = listing.select_one("a") or listing.select_one(".title a")
                        link = link_elem.get('href', '#') if link_elem else '#'
                        
                        if link.startswith('/'):
                            link = "https://unstop.com" + link
                        elif not link.startswith('http'):
                            link = f"https://unstop.com/opportunity/{abs(hash(title + company)) % 100000}"
                        
                        job_id = abs(hash(title + company + "unstop")) % 1000000
                        
                        internship_data = {
                            "id": f"unstop_{job_id}",
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "Unstop",
                            "posted_date": "Not specified",
                            "deadline": "Not specified"
                        }
                        
                        if not any(existing['id'] == internship_data['id'] for existing in results):
                            results.append(internship_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        continue
                
                time.sleep(1)  # Be respectful
                        
            except Exception as e:
                print(f"⚠️ Error scraping Unstop URL {url}: {e}")
                continue
            
            if len(results) >= 10:
                break
        
        # Fallback: Search for internship-related content
        if len(results) < 3:
            try:
                fallback_url = "https://unstop.com/search?query=internship"
                response = requests.get(fallback_url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for any internship-related links
                all_links = soup.find_all('a', href=True)
                for link in all_links[:30]:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if (len(text) > 10 and 
                        ('intern' in text.lower() or is_tech_related(text)) and
                        ('/internship' in href or '/opportunity' in href or '/jobs' in href)):
                        
                        job_id = abs(hash(text + "unstop_fallback")) % 1000000
                        
                        if not any(existing['id'] == f"unstop_{job_id}" for existing in results):
                            results.append({
                                "id": f"unstop_{job_id}",
                                "title": text,
                                "company": "Various Companies",
                                "link": urljoin("https://unstop.com", href),
                                "source": "Unstop",
                                "posted_date": "Not specified",
                                "deadline": "Not specified"
                            })
                            print(f"✅ Found (fallback): {text}")
                            
                            if len(results) >= 5:
                                break
                            
            except Exception as e:
                print(f"⚠️ Unstop fallback failed: {e}")
                
    except Exception as e:
        print(f"⚠️ Error scraping Unstop: {e}")
    
    print(f"📦 Unstop: Found {len(results)} internships")
    return results

def scrape_glassdoor():
    """Scrape internships from Indeed and LinkedIn (better alternatives to Glassdoor)"""
    print("🔍 Scraping Indeed & Alternative Sources...")
    
    results = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate'
        }
        
        # Indeed URLs (more reliable than Glassdoor)
        indeed_searches = [
            ("software+developer+internship", "India"),
            ("data+science+internship", "India"),
            ("python+internship", "India"),
            ("ui+ux+internship", "India"),
            ("business+development+internship", "India"),
            ("machine+learning+internship", "India")
        ]
        
        for search_term, location in indeed_searches:
            try:
                url = f"https://in.indeed.com/jobs?q={search_term}&l={location}&sort=date"
                print(f"   Checking Indeed for: {search_term.replace('+', ' ')}")
                
                session = requests.Session()
                session.headers.update(headers)
                
                response = session.get(url, timeout=15)
                
                if response.status_code != 200:
                    print(f"   Status code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Try multiple selectors for Indeed listings
                selectors_to_try = [
                    "[data-jk]",  # Primary Indeed job selector
                    ".jobsearch-SerpJobCard",
                    ".job_seen_beacon",
                    ".result",
                    ".slider_container .slider_item",
                    "[class*='job']"
                ]
                
                listings = []
                for selector in selectors_to_try:
                    listings = soup.select(selector)
                    if listings:
                        print(f"   Found {len(listings)} listings with selector: {selector}")
                        break
                
                for listing in listings[:8]:
                    try:
                        # Extract title
                        title = None
                        title_selectors = [
                            "h2 a span[title]",
                            "h2 a[data-jk]",
                            ".jobTitle a",
                            ".jobTitle span",
                            "a[data-jk] span",
                            "h2 span",
                            "[data-testid='job-title']"
                        ]
                        
                        for selector in title_selectors:
                            title_elem = listing.select_one(selector)
                            if title_elem:
                                title = title_elem.get_text(strip=True) or title_elem.get('title', '').strip()
                                if title and len(title) > 5:
                                    break
                        
                        if not title:
                            continue
                        
                        # Extract company
                        company = None
                        company_selectors = [
                            "[data-testid='company-name']",
                            ".companyName",
                            ".company",
                            "span.companyName a",
                            "span.companyName"
                        ]
                        
                        for selector in company_selectors:
                            company_elem = listing.select_one(selector)
                            if company_elem:
                                company = company_elem.get_text(strip=True)
                                if company:
                                    break
                        
                        company = company or "Company Name Not Listed"
                        
                        # Check relevance
                        if not (is_tech_related(title, company) or 'intern' in title.lower()):
                            continue
                        
                        # Extract link
                        link_elem = listing.select_one("h2 a") or listing.select_one("a[data-jk]")
                        link = link_elem.get('href', '#') if link_elem else '#'
                        
                        if link.startswith('/'):
                            link = "https://in.indeed.com" + link
                        elif not link.startswith('http'):
                            # Generate Indeed link format
                            jk = listing.get('data-jk', '') or abs(hash(title + company)) % 1000000
                            link = f"https://in.indeed.com/viewjob?jk={jk}"
                        
                        job_id = abs(hash(title + company + "indeed")) % 1000000
                        
                        internship_data = {
                            "id": f"indeed_{job_id}",
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "Indeed",
                            "posted_date": "Not specified",
                            "deadline": "Not specified"
                        }
                        
                        if not any(existing['id'] == internship_data['id'] for existing in results):
                            results.append(internship_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        continue
                
                time.sleep(1)  # Rate limiting
                        
            except Exception as e:
                print(f"⚠️ Error with Indeed search {search_term}: {e}")
                continue
                
            if len(results) >= 8:
                break
        
        # Try AngelList/Wellfound for startup internships
        if len(results) < 5:
            try:
                angel_url = "https://angel.co/jobs"
                response = requests.get(angel_url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for job listings on AngelList
                job_links = soup.find_all('a', href=True)
                for link in job_links[:20]:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')
                    
                    if (len(text) > 10 and 
                        ('intern' in text.lower() or is_tech_related(text)) and
                        ('/jobs/' in href or '/job/' in href)):
                        
                        job_id = abs(hash(text + "angel")) % 1000000
                        
                        if not any(existing['id'] == f"angel_{job_id}" for existing in results):
                            results.append({
                                "id": f"angel_{job_id}",
                                "title": text,
                                "company": "Startup Companies",
                                "link": urljoin("https://angel.co", href),
                                "source": "AngelList",
                                "posted_date": "Not specified",
                                "deadline": "Not specified"
                            })
                            print(f"✅ Found (AngelList): {text}")
                            
                            if len(results) >= 8:
                                break
                            
            except Exception as e:
                print(f"⚠️ AngelList scraping failed: {e}")
        
        # Try Freshersworld as additional source
        if len(results) < 5:
            try:
                fresher_url = "https://www.freshersworld.com/internships"
                response = requests.get(fresher_url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for job listings
                job_elements = soup.find_all('a', 'div', class_=lambda x: x and ('job' in x.lower() or 'intern' in x.lower()))
                for element in job_elements[:15]:
                    text = element.get_text(strip=True)
                    
                    if (len(text) > 10 and 
                        ('intern' in text.lower() or is_tech_related(text))):
                        
                        job_id = abs(hash(text + "fresher")) % 1000000
                        
                        if not any(existing['id'] == f"fresher_{job_id}" for existing in results):
                            href = element.get('href', '') if element.name == 'a' else '#'
                            link = urljoin("https://www.freshersworld.com", href) if href else "https://www.freshersworld.com/internships"
                            
                            results.append({
                                "id": f"fresher_{job_id}",
                                "title": text,
                                "company": "Various Companies",
                                "link": link,
                                "source": "FreshersWorld",
                                "posted_date": "Not specified",
                                "deadline": "Not specified"
                            })
                            print(f"✅ Found (FreshersWorld): {text}")
                            
                            if len(results) >= 8:
                                break
                            
            except Exception as e:
                print(f"⚠️ FreshersWorld scraping failed: {e}")
                
    except Exception as e:
        print(f"⚠️ Error in alternative sources scraping: {e}")
    
    print(f"📦 Indeed & Alternative Sources: Found {len(results)} internships")
    return results

def scrape_linkedin_jobs():
    """Scrape publicly available job listings from LinkedIn"""
    print("🔍 Scraping LinkedIn Jobs...")
    
    results = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        # LinkedIn job search URLs for internships
        linkedin_searches = [
            "software%20engineer%20internship",
            "data%20science%20internship", 
            "python%20internship",
            "machine%20learning%20internship",
            "business%20development%20internship"
        ]
        
        for search_term in linkedin_searches:
            try:
                # Use LinkedIn's public job search
                url = f"https://www.linkedin.com/jobs/search?keywords={search_term}&location=India&distance=25&f_JT=I&f_E=1%2C2"
                print(f"   Checking LinkedIn for: {search_term.replace('%20', ' ')}")
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code != 200:
                    print(f"   Status code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # LinkedIn job listing selectors
                selectors_to_try = [
                    ".job-search-card",
                    ".jobs-search__results-list li",
                    "[data-job-id]",
                    ".job-card-container",
                    ".job-card"
                ]
                
                listings = []
                for selector in selectors_to_try:
                    listings = soup.select(selector)
                    if listings:
                        print(f"   Found {len(listings)} listings with selector: {selector}")
                        break
                
                for listing in listings[:6]:
                    try:
                        # Extract title
                        title = None
                        title_selectors = [
                            ".job-search-card__title a",
                            ".sr-only",
                            "h3 a",
                            ".job-title",
                            "a[data-tracking-control-name='public_jobs_jserp-result_search-card']"
                        ]
                        
                        for selector in title_selectors:
                            title_elem = listing.select_one(selector)
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                if title and len(title) > 5 and not title.startswith('Show more'):
                                    break
                        
                        if not title:
                            continue
                        
                        # Extract company
                        company = None
                        company_selectors = [
                            ".job-search-card__subtitle-link",
                            ".job-card-container__company-name",
                            "h4 a",
                            ".company-name"
                        ]
                        
                        for selector in company_selectors:
                            company_elem = listing.select_one(selector)
                            if company_elem:
                                company = company_elem.get_text(strip=True)
                                if company:
                                    break
                        
                        company = company or "Company Name Not Listed"
                        
                        # Check relevance
                        if not (is_tech_related(title, company) or 'intern' in title.lower()):
                            continue
                        
                        # Extract link
                        link_elem = listing.select_one("a") or listing.select_one(".job-search-card__title a")
                        link = link_elem.get('href', '#') if link_elem else '#'
                        
                        if link.startswith('/'):
                            link = "https://www.linkedin.com" + link
                        elif not link.startswith('http'):
                            link = f"https://www.linkedin.com/jobs/view/{abs(hash(title + company)) % 1000000}"
                        
                        # Extract dates
                        posted_date = "Not specified"
                        deadline = "Not specified"
                        
                        try:
                            # Look for LinkedIn date elements
                            date_elements = listing.select(".job-search-card__listitem time, .job-posting-date, time")
                            for date_elem in date_elements:
                                date_text = date_elem.get_text(strip=True)
                                if date_text and len(date_text) > 2:
                                    posted_date = date_text
                                    break
                            
                            # Look for any time-related text
                            time_texts = listing.find_all(string=True)
                            for text in time_texts:
                                text = text.strip()
                                if any(keyword in text.lower() for keyword in ['ago', 'posted', 'days', 'hours', 'weeks']):
                                    if 'ago' in text.lower() or 'posted' in text.lower():
                                        posted_date = text
                                        break
                        except:
                            pass
                        
                        job_id = abs(hash(title + company + "linkedin")) % 1000000
                        
                        internship_data = {
                            "id": f"linkedin_{job_id}",
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "LinkedIn",
                            "posted_date": posted_date,
                            "deadline": deadline
                        }
                        
                        if not any(existing['id'] == internship_data['id'] for existing in results):
                            results.append(internship_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        continue
                
                time.sleep(2)  # LinkedIn is strict about rate limiting
                        
            except Exception as e:
                print(f"⚠️ Error with LinkedIn search {search_term}: {e}")
                continue
                
            if len(results) >= 6:
                break
                
    except Exception as e:
        print(f"⚠️ Error scraping LinkedIn: {e}")
    
    print(f"📦 LinkedIn: Found {len(results)} internships")
    return results


def scrape_timesjobs():
    """Scrape internships from TimesJobs"""
    print("🔍 Scraping TimesJobs...")
    
    results = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        # TimesJobs search URLs
        timesjobs_searches = [
            "software+developer+intern",
            "data+science+intern",
            "python+intern",
            "business+development+intern"
        ]
        
        for search_term in timesjobs_searches:
            try:
                url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={search_term}&txtLocation=India"
                print(f"   Checking TimesJobs for: {search_term.replace('+', ' ')}")
                
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code != 200:
                    print(f"   Status code: {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # TimesJobs listing selectors
                listings = soup.select(".srp-jobtitle-wrap") or soup.select(".job-bx") or soup.select(".joblist-comp-name")
                
                for listing in listings[:5]:
                    try:
                        # Extract title
                        title_elem = listing.select_one("h2 a") or listing.select_one(".joblist-comp-name a") or listing.select_one("a")
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        if not title or len(title) < 5:
                            continue
                        
                        # Extract company
                        company_elem = listing.select_one(".joblist-comp-name") or listing.select_one(".comp-name")
                        company = company_elem.get_text(strip=True) if company_elem else "Company Name Not Listed"
                        
                        # Check relevance
                        if not (is_tech_related(title, company) or 'intern' in title.lower()):
                            continue
                        
                        # Extract link
                        link = title_elem.get('href', '#')
                        if not link.startswith('http'):
                            link = f"https://www.timesjobs.com/{link}" if link.startswith('/') else f"https://www.timesjobs.com/job-detail/{abs(hash(title + company)) % 100000}"
                        
                        # Extract dates
                        posted_date = "Not specified"
                        deadline = "Not specified"
                        
                        try:
                            # Look for TimesJobs date elements
                            date_elements = listing.select(".date, .posted-date, .last-date, .apply-by")
                            for date_elem in date_elements:
                                date_text = date_elem.get_text(strip=True)
                                if 'posted' in date_text.lower() or 'ago' in date_text.lower():
                                    posted_date = date_text
                                elif 'last date' in date_text.lower() or 'apply by' in date_text.lower():
                                    deadline = date_text
                            
                            # Look for text patterns in the listing
                            all_text = listing.get_text()
                            import re
                            # Look for patterns like "Posted: 2 days ago" or "Apply by: 15 Jan"
                            posted_match = re.search(r'posted:?\s*([^|]*(?:ago|[0-9]{1,2}[/-][0-9]{1,2}))', all_text, re.IGNORECASE)
                            if posted_match:
                                posted_date = posted_match.group(1).strip()
                            
                            deadline_match = re.search(r'(?:apply by|last date|deadline):?\s*([^|]*(?:[0-9]{1,2}[/-][0-9]{1,2}|[a-z]{3,}))', all_text, re.IGNORECASE)
                            if deadline_match:
                                deadline = deadline_match.group(1).strip()
                        except:
                            pass
                        
                        job_id = abs(hash(title + company + "timesjobs")) % 1000000
                        
                        internship_data = {
                            "id": f"timesjobs_{job_id}",
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "TimesJobs",
                            "posted_date": posted_date,
                            "deadline": deadline
                        }
                        
                        if not any(existing['id'] == internship_data['id'] for existing in results):
                            results.append(internship_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        continue
                
                time.sleep(1)
                        
            except Exception as e:
                print(f"⚠️ Error with TimesJobs search {search_term}: {e}")
                continue
                
            if len(results) >= 5:
                break
                
    except Exception as e:
        print(f"⚠️ Error scraping TimesJobs: {e}")
    
    print(f"📦 TimesJobs: Found {len(results)} internships")
    return results


def scrape_shine():
    """Scrape internships from Shine.com"""
    print("🔍 Scraping Shine...")
    
    results = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        # Shine search URLs
        shine_searches = [
            "software+developer+internship",
            "data+science+internship", 
            "python+internship"
        ]
        
        for search_term in shine_searches:
            try:
                url = f"https://www.shine.com/job-search/{search_term}/jobs-in-india"
                print(f"   Checking Shine for: {search_term.replace('+', ' ')}")
                
                response = requests.get(url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Shine listing selectors
                listings = soup.select(".jobCard") or soup.select(".job-card") or soup.select(".result-set")
                
                for listing in listings[:5]:
                    try:
                        # Extract title
                        title_elem = listing.select_one("h2 a") or listing.select_one(".job-title a") or listing.select_one("a")
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        if not title or len(title) < 5:
                            continue
                        
                        # Extract company
                        company_elem = listing.select_one(".company") or listing.select_one(".comp-name")
                        company = company_elem.get_text(strip=True) if company_elem else "Company Name Not Listed"
                        
                        # Check relevance
                        if not (is_tech_related(title, company) or 'intern' in title.lower()):
                            continue
                        
                        # Extract link
                        link = title_elem.get('href', '#')
                        if link.startswith('/'):
                            link = "https://www.shine.com" + link
                        elif not link.startswith('http'):
                            link = f"https://www.shine.com/job/{abs(hash(title + company)) % 100000}"
                        
                        job_id = abs(hash(title + company + "shine")) % 1000000
                        
                        internship_data = {
                            "id": f"shine_{job_id}",
                            "title": title,
                            "company": company,
                            "link": link,
                            "source": "Shine",
                            "posted_date": "Not specified",
                            "deadline": "Not specified"
                        }
                        
                        if not any(existing['id'] == internship_data['id'] for existing in results):
                            results.append(internship_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        continue
                
                time.sleep(1)
                        
            except Exception as e:
                print(f"⚠️ Error with Shine search {search_term}: {e}")
                continue
            
            if len(results) >= 4:
                break
                
    except Exception as e:
        print(f"⚠️ Error scraping Shine: {e}")
    
    print(f"📦 Shine: Found {len(results)} internships")
    return results

def scrape_foundit():
    """Scrape Foundit.in (formerly Monster India)"""
    print("🔍 Scraping Foundit.in...")
    internships = []
    
    search_terms = ['software engineer intern', 'data science intern', 'python intern', 
                   'web developer intern', 'business development intern']
    
    for term in search_terms:
        try:
            url = f"https://www.foundit.in/srp/results?query={quote(term)}&locations=All+India"
            print(f"   Checking Foundit for: {term}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Foundit job cards
                job_cards = soup.find_all(['div'], class_=['jobTuple', 'job-tuple', 'srpResultCardContainer'])
                
                for card in job_cards[:5]:  # Limit to first 5 results
                    try:
                        title_elem = card.find(['a', 'h3'], class_=['jobTitle', 'job-title'])
                        company_elem = card.find(['span', 'div'], class_=['companyName', 'company-name'])
                        link_elem = card.find('a', href=True)
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            link = urljoin("https://www.foundit.in", link_elem['href']) if link_elem else url
                            
                            if is_tech_related(title, company):
                                internships.append({
                                    'id': f"foundit_{hash(title + company)}",
                                    'title': title,
                                    'company': company,
                                    'link': link,
                                    'source': 'Foundit',
                                    'posted_date': 'Not specified'
                                })
                                print(f"✅ Found: {title} at {company}")
                    except Exception as e:
                        continue
            
            time.sleep(2)  # Respectful delay
            
        except Exception as e:
            print(f"   Error searching {term}: {str(e)}")
            continue
    
    print(f"📦 Foundit: Found {len(internships)} internships")
    return internships

def scrape_freshersworld():
    """Scrape FreshersWorld.com"""
    print("🔍 Scraping FreshersWorld...")
    internships = []
    
    try:
        url = "https://www.freshersworld.com/jobs/jobsearch/internship-jobs"
        print(f"   Checking: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # FreshersWorld job listings
            job_cards = soup.find_all(['div', 'article'], class_=['job-container', 'job-card', 'listContainer'])
            
            for card in job_cards[:10]:  # Limit to first 10
                try:
                    title_elem = card.find(['h3', 'h4', 'a'], class_=['job-title', 'jobTitle'])
                    company_elem = card.find(['span', 'div'], class_=['company', 'companyName'])
                    link_elem = card.find('a', href=True)
                    
                    if title_elem and company_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        link = urljoin("https://www.freshersworld.com", link_elem['href']) if link_elem else url
                        
                        if is_tech_related(title, company):
                            internships.append({
                                'id': f"freshersworld_{hash(title + company)}",
                                'title': title,
                                'company': company,
                                'link': link,
                                'source': 'FreshersWorld',
                                'posted_date': 'Not specified'
                            })
                            print(f"✅ Found: {title} at {company}")
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"   Error scraping FreshersWorld: {str(e)}")
    
    print(f"📦 FreshersWorld: Found {len(internships)} internships")
    return internships

def scrape_instahyre():
    """Scrape Instahyre.com"""
    print("🔍 Scraping Instahyre...")
    internships = []
    
    try:
        url = "https://www.instahyre.com/search-jobs/?q=intern"
        print(f"   Checking: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Instahyre job cards
            job_cards = soup.find_all(['div'], class_=['job-card', 'opportunity-card'])
            
            for card in job_cards[:8]:  # Limit to first 8
                try:
                    title_elem = card.find(['h2', 'h3'], class_=['job-title'])
                    company_elem = card.find(['span', 'div'], class_=['company-name'])
                    link_elem = card.find('a', href=True)
                    
                    if title_elem and company_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        link = urljoin("https://www.instahyre.com", link_elem['href']) if link_elem else url
                        
                        if is_tech_related(title, company):
                            internships.append({
                                'id': f"instahyre_{hash(title + company)}",
                                'title': title,
                                'company': company,
                                'link': link,
                                'source': 'Instahyre',
                                'posted_date': 'Not specified'
                            })
                            print(f"✅ Found: {title} at {company}")
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"   Error scraping Instahyre: {str(e)}")
    
    print(f"📦 Instahyre: Found {len(internships)} internships")
    return internships

def scrape_wellfound():
    """Scrape Wellfound (formerly AngelList)"""
    print("🔍 Scraping Wellfound...")
    internships = []
    
    try:
        url = "https://wellfound.com/jobs?role=internship"
        print(f"   Checking: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Wellfound job listings
            job_cards = soup.find_all(['div'], class_=['job', 'startup-job'])
            
            for card in job_cards[:8]:  # Limit to first 8
                try:
                    title_elem = card.find(['h2', 'h3', 'a'])
                    company_elem = card.find(['span'], class_=['company'])
                    link_elem = card.find('a', href=True)
                    
                    if title_elem and company_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        link = urljoin("https://wellfound.com", link_elem['href']) if link_elem else url
                        
                        if is_tech_related(title, company):
                            internships.append({
                                'id': f"wellfound_{hash(title + company)}",
                                'title': title,
                                'company': company,
                                'link': link,
                                'source': 'Wellfound',
                                'posted_date': 'Not specified'
                            })
                            print(f"✅ Found: {title} at {company}")
                except Exception as e:
                    continue
                    
    except Exception as e:
        print(f"   Error scraping Wellfound: {str(e)}")
    
    print(f"📦 Wellfound: Found {len(internships)} internships")
    return internships

# ...existing code...

def scrape_all():
    """Scrape from all sources and combine results"""
    print("\nStarting comprehensive internship search...")
    
    all_results = []
    
    # Scrape from all sources (with error handling for each)
    try:
        all_results.extend(scrape_internshala())
    except Exception as e:
        print(f"⚠️ Internshala failed: {e}")
    
    try:
        all_results.extend(scrape_naukri())
    except Exception as e:
        print(f"⚠️ Naukri failed: {e}")
    
    try:
        all_results.extend(scrape_unstop())
    except Exception as e:
        print(f"⚠️ Unstop failed: {e}")
    
    try:
        all_results.extend(scrape_glassdoor())
    except Exception as e:
        print(f"⚠️ Indeed/Alternative sources failed: {e}")
    
    try:
        all_results.extend(scrape_linkedin_jobs())
    except Exception as e:
        print(f"⚠️ LinkedIn failed: {e}")
    
    try:
        all_results.extend(scrape_timesjobs())
    except Exception as e:
        print(f"⚠️ TimesJobs failed: {e}")
    
    try:
        all_results.extend(scrape_shine())
    except Exception as e:
        print(f"⚠️ Shine failed: {e}")
    
    try:
        all_results.extend(scrape_foundit())
    except Exception as e:
        print(f"⚠️ Foundit failed: {e}")
    
    try:
        all_results.extend(scrape_freshersworld())
    except Exception as e:
        print(f"⚠️ FreshersWorld failed: {e}")
    
    try:
        all_results.extend(scrape_instahyre())
    except Exception as e:
        print(f"⚠️ Instahyre failed: {e}")
    
    try:
        all_results.extend(scrape_wellfound())
    except Exception as e:
        print(f"⚠️ Wellfound failed: {e}")
    
    # Additional job portals would go here
    # (Keeping for future expansion)
    
    # New websites
    try:
        all_results.extend(scrape_foundit())
    except Exception as e:
        print(f"⚠️ Foundit failed: {e}")
    
    try:
        all_results.extend(scrape_freshersworld())
    except Exception as e:
        print(f"⚠️ FreshersWorld failed: {e}")
    
    try:
        all_results.extend(scrape_instahyre())
    except Exception as e:
        print(f"⚠️ Instahyre failed: {e}")
    
    try:
        all_results.extend(scrape_wellfound())
    except Exception as e:
        print(f"⚠️ Wellfound failed: {e}")
    
    # Remove duplicates by job id and similar titles
    unique_results = {}
    for job in all_results:
        # Use ID as primary key
        if job['id'] not in unique_results:
            unique_results[job['id']] = job
    
    final_results = list(unique_results.values())
    
    print(f"\n📊 SUMMARY:")
    print(f"Total unique internships found: {len(final_results)}")
    
    # Group by source for summary
    source_counts = {}
    for job in final_results:
        source = job.get('source', 'Unknown')
        source_counts[source] = source_counts.get(source, 0) + 1
    
    for source, count in source_counts.items():
        print(f"  {source}: {count} internships")
    
    # Sort by source for better organization
    final_results.sort(key=lambda x: x.get('source', 'Unknown'))
    
    return final_results
