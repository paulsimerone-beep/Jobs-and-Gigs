import re
import json

# Read the extracted content
with open('extracted_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split content by page markers
pages = re.split(r'--- Page \d+ ---', content)

jobs = []
job_id = 1000  # Start IDs from 1000 to avoid conflicts

for page in pages[1:]:  # Skip first empty page
    # Try to extract job listings
    sections = page.split('================================================================================')
    
    for section in sections:
        section = section.strip()
        if len(section) < 100:
            continue
        
        # Look for job posting patterns
        lines = section.split('\n')
        job_text = '\n'.join(lines)
        
        # Extract key information
        title = None
        company = None
        location = None
        job_type = "full-time"
        salary = "Negotiable"
        description = ""
        
        # Find location (usually contains "Location:" or city names)
        location_match = re.search(r'(?:Location|Based):\s*([^\n]+)', section)
        if location_match:
            location = location_match.group(1).strip()
        
        # Extract title from the first few lines
        first_line = lines[0].strip() if lines else ""
        if first_line and len(first_line) > 5:
            title = first_line
        
        # Extract company name
        company_match = re.search(r'(?:Company|About\s+)([A-Z][^\n]+?)(?:\n|$)', section)
        if company_match:
            company = company_match.group(1).strip()
        elif "Studio 88" in section:
            company = "Studio 88"
        elif "OUTsurance" in section:
            company = "OUTsurance"
        elif "Impala Platinum" in section:
            company = "Impala Platinum"
        elif "Sasol" in section:
            company = "Sasol"
        elif "Shoprite" in section:
            company = "Shoprite"
        
        # Get salary/Employment type info
        emp_type_match = re.search(r'(?:Employment Type|Type):\s*([^\n]+)', section)
        if emp_type_match:
            emp_text = emp_type_match.group(1).strip().lower()
            if 'permanent' in emp_text or 'full' in emp_text:
                job_type = "full-time"
            elif 'contract' in emp_text:
                job_type = "contract"
            elif 'part' in emp_text:
                job_type = "part-time"
        
        # Extract salary
        salary_match = re.search(r'(?:Salary|Remuneration):\s*([^\n]+)', section)
        if salary_match:
            salary = salary_match.group(1).strip()
        
        # Build description from first few sentences/paragraphs
        desc_lines = []
        in_description = False
        for i, line in enumerate(lines):
            if any(x in line for x in ['Responsibilities', 'About', 'Purpose', 'Overview', 'Role']):
                in_description = True
            if in_description and line.strip():
                if line.strip().startswith('•') or not any(x in line for x in ['Location', 'Qualification', 'Experience', 'Salary']):
                    desc_lines.append(line.strip())
                if len(desc_lines) >= 2:
                    break
        
        description = ' '.join(desc_lines[:2]) if desc_lines else section[:150]
        description = description.replace('•', '').strip()[:150]
        
        # Only add if we have meaningful data
        if title and len(title) > 5 and company:
            job = {
                "id": job_id,
                "title": title,
                "company": company,
                "location": location or "South Africa",
                "salary": salary,
                "description": description[:200],
                "jobType": job_type,
                "workLocation": "on-site",
                "salaryRange": "mid",
                "postedDate": "Jul 2026",
                "contactEmail": f"careers@{company.lower().replace(' ', '')}.co.za"
            }
            jobs.append(job)
            job_id += 1

# Print JavaScript-ready job objects
print("Found", len(jobs), "jobs")
print("\n// PDF Jobs Array:")
print("let pdfJobs = [")
for job in jobs[:20]:  # First 20 jobs
    print(f"    {{")
    print(f"        id: {job['id']},")
    print(f"        title: \"{job['title']}\",")
    print(f"        company: \"{job['company']}\",")
    print(f"        location: \"{job['location']}\",")
    print(f"        salary: \"{job['salary']}\",")
    print(f"        description: \"{job['description']}\",")
    print(f"        jobType: \"{job['jobType']}\",")
    print(f"        workLocation: \"{job['workLocation']}\",")
    print(f"        salaryRange: \"{job['salaryRange']}\",")
    print(f"        postedDate: \"Jul 2026\",")
    print(f"        contactEmail: \"{job['contactEmail']}\"")
    print(f"    }},")
print("];")

# Also save as JSON for reference
with open('pdf_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(jobs, f, indent=2)

print(f"\nSaved {len(jobs)} jobs to pdf_jobs.json")
