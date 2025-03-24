import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.jobly.fi/tyopaikat?search=it&job_geo_location=&Etsi+ty%C3%B6paikkoja=Etsi+ty%C3%B6paikkoja&lat=&lon=&country=&administrative_area_level_1='

response = requests.get(url)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('a', class_='search_result_row', limit=15)

    job_data = []

    for job in jobs:
        
        data_title = job.find('title', class_='recruiter-job-link recruiter-jobs-new-tab-processed')
        data_date = job.find('span', class_='date')  
        data_company = job.find('span', class_='recruiter-company-profile-job-organization')
        
        data_location = job.find('span', class_='location')

        job_data.append({
            'Job title': data_title.text if data_title else None,
            'Date': data_date.text if data_date else None,
            'Company': data_company.text if data_company else None,
            'Location': data_location.text if data_location else None,
        })

    for job in job_data:
        print(f"Job title: {job['Job title']}")
        print(f"Date: {job['Date']}")
        print(f"Company: {job['Company']}")
        print(f"Location: {job['Location']}\n")

    df = pd.DataFrame(job_data)
    df.to_excel('job_scraping.xlsx', index=False)

    print("Data saved to job_scraping.xlsx")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")