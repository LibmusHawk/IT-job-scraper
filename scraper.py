import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

url = 'https://www.jobly.fi/tyopaikat?search=it'

response = requests.get(url)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = soup.find_all('div', class_='views-row')[:10]

    job_data = []

    for job in jobs:
        
        data_title = job.find('h2', class_='node__title')
        data_date = job.find('span', class_='date')  
        data_company = job.find('span', class_='recruiter-company-profile-job-organization')
        data_location = job.find('div', class_='location')
        
        
        img_tag = job.find('img', class_=lambda x: x and 'lazyload' in x.lower())
        img_url = (img_tag.get('data-src') or img_tag.get('src')).split('>')[0].strip() if img_tag else None
        img_url = urljoin(url, img_url) if img_url and not img_url.startswith('http') else img_url

        job_data.append({
            'Job title': data_title.text.strip() if data_title else None,
            'Date': data_date.text.strip() if data_date else None,
            'Company': data_company.text.strip() if data_company else None,
            'Location': data_location.text.strip() if data_location else None,
            'Image URL': img_url if img_url else None
        })

    print("\n" + "="*60)
    print(f"FOUND {len(job_data)} JOB LISTINGS".center(60))
    print("="*60 + "\n")
    
    for job in job_data:
        print('-'*60 + "")
        print(f"Job title: {job['Job title']}")
        print(f"Date: {job['Date']}")
        print(f"Company: {job['Company']}")
        print(f"Location: {job['Location']}")
        print(f"Image: {job['Image URL']}")
        print('-'*60 + "\n")

    df = pd.DataFrame(job_data)
    df.to_excel('job_scraping.xlsx', index=False)

    print("Data saved to job_scraping.xlsx")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")