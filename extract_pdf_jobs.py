from pathlib import Path
import json
import re
from PyPDF2 import PdfReader

pdf_path = r"C:\Users\TK\OneDrive\Desktop\Job listing 001.pdf"
workspace = Path(r"c:\Users\TK\OneDrive\First website")
out_dir = workspace / "pdf_images"
out_dir.mkdir(exist_ok=True)

reader = PdfReader(pdf_path)
pages = list(reader.pages)
image_pages = [idx for idx, page in enumerate(pages, 1) if page.images]
jobs = []


def pick_apply_url(text: str) -> str:
    urls = [u.rstrip(').,;:') for u in re.findall(r'https?://\S+', text)]
    if not urls:
        return ""
    for url in urls:
        lower = url.lower()
        if any(token in lower for token in ['apply', 'candidateapp', 'vacancy', 'recruit', 'careers', 'erecruit']):
            return url
    return urls[0]


for posting_index, start_page in enumerate(image_pages):
    end_page = image_pages[posting_index + 1] - 1 if posting_index + 1 < len(image_pages) else len(pages)
    combined_text_parts = []
    for page_num in range(start_page, end_page + 1):
        combined_text_parts.append((pages[page_num - 1].extract_text() or ""))
    combined_text = "\n".join(combined_text_parts)
    lines = [ln.strip() for ln in combined_text.splitlines() if ln.strip()]

    title = None
    title_keywords = ['engineer', 'analyst', 'manager', 'worker', 'cashier', 'assistant', 'therapist', 'auditor', 'advisor', 'lead', 'specialist', 'supervisor', 'executive', 'broker', 'operator', 'developer', 'officer', 'coordinator', 'consultant', 'recruiter', 'trainer', 'driver', 'clerk', 'administrator', 'designer']

    for line in lines[:25]:
        clean = line.replace('•', '').strip()
        lower = clean.lower()
        if not clean or len(clean) > 140:
            continue
        if any(skip in lower for skip in ['closing date', 'reference', 'for more', 'location:', 'application', 'https://', 'company overview', 'what you get', 'requirements', 'qualifications', 'responsibilities', 'experience', 'key responsibilities', 'about the role', 'skills', 'benefits', 'department:', 'industry:', 'division:', 'reports to', 'job type:']):
            continue
        if clean[0].isupper() and ((' – ' in clean or ' - ' in clean) or any(keyword in lower for keyword in title_keywords)):
            title = clean
            break

    if not title:
        title = f"Job {start_page}"

    body_text = "\n".join(lines)

    company = 'PDF Extract'
    lower_text = combined_text.lower()
    if 'shoprite' in lower_text:
        company = 'Shoprite'
    elif 'truworths' in lower_text:
        company = 'Truworths'
    elif 'dis-chem' in lower_text or 'dis chem' in lower_text:
        company = 'Dis-Chem'
    elif 'outsurance' in lower_text:
        company = 'OUTsurance'
    elif 'studio 88' in lower_text:
        company = 'Studio 88'
    elif 'toys r us' in lower_text or 'babies r us' in lower_text:
        company = 'Toys R Us / Babies R Us'
    elif 'impala' in lower_text:
        company = 'Impala Platinum'
    elif 'capitec' in lower_text:
        company = 'Capitec'
    elif 'cashier' in lower_text and 'cape gate' in lower_text:
        company = 'Cape Gate'
    elif 'sasol' in lower_text:
        company = 'Sasol'

    location = 'South Africa'
    location_match = re.search(r'location:\s*([^\n]+)', combined_text, flags=re.IGNORECASE)
    if location_match:
        location = location_match.group(1).strip()
    elif ', cape town' in title.lower():
        location = 'Cape Town'
    elif ', gauteng' in title.lower():
        location = 'Gauteng'
    elif 'bloemfontein' in lower_text:
        location = 'Bloemfontein'
    elif 'centurion' in lower_text:
        location = 'Centurion'
    elif 'darling' in lower_text:
        location = 'Darling'
    elif 'germiston' in lower_text:
        location = 'Germiston'
    elif 'pretoria' in lower_text:
        location = 'Pretoria'
    elif 'cape town' in lower_text:
        location = 'Cape Town'

    salary = 'Negotiable'
    salary_match = re.search(r'salary:\s*([^\n]+)', combined_text, flags=re.IGNORECASE)
    if salary_match:
        salary = salary_match.group(1).strip()

    job_type = 'full-time'
    lower_title = title.lower()
    if 'contract' in lower_title or 'temporary' in lower_title:
        job_type = 'contract'
    elif 'part-time' in lower_title or 'part time' in lower_title:
        job_type = 'part-time'

    page = pages[start_page - 1]
    image_name = f"{start_page}_{page.images[0].name}"
    image_path = out_dir / image_name
    with open(image_path, 'wb') as handle:
        handle.write(page.images[0].data)

    jobs.append({
        'id': 1000 + len(jobs),
        'title': title,
        'company': company,
        'location': location,
        'salary': salary,
        'description': body_text,
        'jobType': job_type,
        'workLocation': 'on-site',
        'salaryRange': 'mid',
        'postedDate': 'Jul 2026',
        'contactEmail': f"careers@{company.lower().replace(' ', '').replace('/', '')}.co.za",
        'image': f"pdf_images/{image_name}",
        'applyUrl': pick_apply_url(combined_text)
    })

with open(workspace / 'pdf_jobs.json', 'w', encoding='utf-8') as handle:
    json.dump(jobs, handle, indent=2)

with open(workspace / 'pdf_jobs.js', 'w', encoding='utf-8') as handle:
    handle.write('window.pdfJobsData = ' + json.dumps(jobs, indent=2) + ';\n')

print(f'Extracted {len(jobs)} job postings from the PDF.')
print(f'Images saved to {out_dir}')
