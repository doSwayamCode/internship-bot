from bs4 import BeautifulSoup
import requests
import re
import time
import json
from urllib.parse import urljoin, quote

# Comprehensive keywords for filtering (including tech and non-tech roles)
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
    
    # Business Development & Marketing
    'business development', 'business analyst', 'business intelligence', 'strategy',
    'market research', 'sales', 'marketing', 'product management', 'product manager',
    'digital marketing', 'social media', 'content marketing', 'growth hacking',
    'brand management', 'advertising', 'promotion', 'campaign', 'lead generation',
    'customer acquisition', 'business strategy', 'market analysis', 'competitive analysis',
    
    # Finance & Accounting
    'finance', 'financial analyst', 'accounting', 'investment', 'banking', 'equity research',
    'financial modeling', 'portfolio management', 'risk management', 'audit', 'taxation',
    'corporate finance', 'financial planning', 'budget', 'cost analysis', 'valuation',
    'trading', 'wealth management', 'insurance', 'credit analysis', 'financial services',
    
    # Human Resources
    'human resource', 'hr', 'talent acquisition', 'recruitment', 'hiring', 'staffing',
    'employee relations', 'compensation', 'benefits', 'training', 'learning development',
    'organizational development', 'performance management', 'payroll', 'hr analytics',
    
    # Operations & Supply Chain
    'operations', 'supply chain', 'logistics', 'procurement', 'vendor management',
    'process improvement', 'quality assurance', 'production', 'manufacturing',
    'project management', 'program management', 'operations research', 'lean', 'six sigma',
    
    # Consulting & Strategy
    'consulting', 'strategy consulting', 'management consulting', 'business consulting',
    'strategy', 'strategic planning', 'business transformation', 'change management',
    'process consulting', 'operational consulting', 'advisory', 'client engagement',
    
    # Sales & Customer Success
    'sales', 'sales development', 'account management', 'customer success', 'customer service',
    'client relations', 'business development', 'partnership', 'channel sales',
    'inside sales', 'field sales', 'retail', 'customer experience', 'crm',
    
    # Content & Communications
    'content', 'content writing', 'copywriting', 'communications', 'public relations',
    'journalism', 'editorial', 'blogging', 'social media management', 'community management',
    'marketing communications', 'internal communications', 'corporate communications',
    
    # Legal & Compliance
    'legal', 'law', 'compliance', 'regulatory', 'contract', 'legal research',
    'paralegal', 'corporate law', 'intellectual property', 'litigation', 'legal affairs',
    
    # Research & Analytics (Non-Tech)
    'research', 'market research', 'policy research', 'economic research', 'survey research',
    'primary research', 'secondary research', 'research analyst', 'insights', 'analytics',
    
    # Non-Tech Specialized Roles
    'esg', 'environmental social governance', 'sustainability', 'ccass', 'compliance',
    'environment engineer', 'environmental engineering', 'climate', 'carbon',
    'renewable energy', 'green technology', 'corporate social responsibility',
    'risk management', 'audit', 'finance', 'consulting', 'research', 'policy',
    
    # General Business & Admin
    'business', 'administration', 'office', 'coordinator', 'assistant', 'associate',
    'analyst', 'specialist', 'executive', 'manager', 'trainee', 'graduate',
    'entry level', 'fresher', 'junior', 'intern', 'internship'
]

def is_relevant_internship(title, company=""):
    """Check if internship is relevant based on title and company (includes both tech and non-tech roles)"""
    text_to_check = f"{title} {company}".lower()
    
    for keyword in TECH_KEYWORDS:
        if keyword.lower() in text_to_check:
            return True
    return False

def scrape_internshala():
    """Scrape tech internships from Internshala"""
    print("Scraping Internshala...")
    
    # Search for specific categories on Internshala (both tech and non-tech)
    tech_urls = [
        # Tech categories
        "https://internshala.com/internships/computer-science",
        "https://internshala.com/internships/web-development", 
        "https://internshala.com/internships/software-development",
        "https://internshala.com/internships/data-science",
        "https://internshala.com/internships/android-app-development",
        "https://internshala.com/internships/python",
        "https://internshala.com/internships/machine-learning",
        "https://internshala.com/internships/artificial-intelligence",
        "https://internshala.com/internships/ui-ux-design",
        
        # Non-tech categories
        "https://internshala.com/internships/business-development",
        "https://internshala.com/internships/marketing",
        "https://internshala.com/internships/finance",
        "https://internshala.com/internships/human-resources",
        "https://internshala.com/internships/sales",
        "https://internshala.com/internships/content-writing",
        "https://internshala.com/internships/consulting",
        "https://internshala.com/internships/operations",
        "https://internshala.com/internships/research",
        "https://internshala.com/internships/analytics",
        "https://internshala.com/internships/administration",
        "https://internshala.com/internships/business-analyst",
        
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

                # Include relevant internships (broader criteria now)
                if not (is_relevant_internship(title, company) or 'intern' in title.lower() or 'trainee' in title.lower()):
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

    print(f"📦 Internshala: Found {len(results)} internships")
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
        
        # LinkedIn job search URLs for internships (both tech and non-tech)
        linkedin_searches = [
            # Tech searches
            "software%20engineer%20internship",
            "data%20science%20internship", 
            "python%20internship",
            "machine%20learning%20internship",
            
            # Non-tech searches
            "business%20development%20internship",
            "marketing%20internship",
            "finance%20internship",
            "consulting%20internship",
            "sales%20internship",
            "human%20resources%20internship",
            "operations%20internship",
            "research%20internship"
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
                        if not (is_relevant_internship(title, company) or 'intern' in title.lower()):
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
        
        # TimesJobs search URLs (both tech and non-tech)
        timesjobs_searches = [
            # Tech searches
            "software+developer+intern",
            "data+science+intern",
            "python+intern",
            
            # Non-tech searches
            "business+development+intern",
            "marketing+intern",
            "finance+intern", 
            "sales+intern",
            "hr+intern",
            "consulting+intern",
            "operations+intern"
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
                        if not (is_relevant_internship(title, company) or 'intern' in title.lower()):
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


def scrape_all():
    """Scrape from all working sources and combine results"""
    print("\nStarting comprehensive internship search...")
    
    all_results = []
    
    # Scrape from working sources only (with error handling for each)
    try:
        all_results.extend(scrape_internshala())
    except Exception as e:
        print(f"⚠️ Internshala failed: {e}")
    
    try:
        all_results.extend(scrape_linkedin_jobs())
    except Exception as e:
        print(f"⚠️ LinkedIn failed: {e}")
    
    try:
        all_results.extend(scrape_timesjobs())
    except Exception as e:
        print(f"⚠️ TimesJobs failed: {e}")
    
    # NEW: Scrape company career opportunities
    try:
        from company_job_aggregator import scrape_company_careers
        career_jobs = scrape_company_careers()
        all_results.extend(career_jobs)
        print(f"✅ Company Careers: Found {len(career_jobs)} positions")
    except Exception as e:
        print(f"⚠️ Company Careers failed: {e}")
    
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
