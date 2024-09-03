import requests
from bs4 import BeautifulSoup
import os

urls = [
    'https://www.prospects.ac.uk/job-profiles/browse-sector/public-services-and-administration',
    "https://www.prospects.ac.uk/job-profiles/browse-sector/creative-arts-and-design",
    'https://www.prospects.ac.uk/job-profiles/browse-sector/information-technology',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/law',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/accountancy-banking-and-finance',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/property-and-construction',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/leisure-sport-and-tourism',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/healthcare',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/environment-and-agriculture',
    'https://www.prospects.ac.uk/job-profiles/browse-sector/public-services-and-administration'

]


def scrape_job_profiles(urls):
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        job_titles = soup.find_all('div', class_='section-item-title')

        main_category_name = url.rsplit('/', 1)[-1]
        main_category_dir = os.path.join('job_profil', main_category_name)
        os.makedirs(main_category_dir, exist_ok=True)

        for job in job_titles:
            job_name = job.text.strip()
            job_url_name = job_name.replace(' ', '-').replace("'", '').replace(",", '')
            job_url_name = job_url_name.replace("(", '').replace(")", '')
            job_dir_name = job_name.lower().replace(' ', '_')

            job_dir = os.path.join(main_category_dir, job_dir_name)
            os.makedirs(job_dir, exist_ok=True)

            job_profile_url = f'https://www.prospects.ac.uk/job-profiles/{job_url_name}'
            response = requests.get(job_profile_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            skills = extract_skills(soup)
            save_to_file(skills, os.path.join(job_dir, 'skills.txt'))

            responsibilities = extract_responsibilities(soup)
            save_to_file(responsibilities, os.path.join(job_dir, 'responsibilities.txt'))

def extract_skills(soup):
    skills_section = soup.find('h2', id='skills').find_next_sibling('ul')
    return [li.get_text(strip=True) for li in skills_section.find_all('li')]

def extract_responsibilities(soup):
    responsibilities_section = soup.find('h2', id='responsibilities').find_next_sibling('ul')
    return [li.get_text(strip=True) for li in responsibilities_section.find_all('li')]

def save_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(item + '\n')


for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_titles = soup.find_all('div', class_='section-item-title')

    main_category_name = url.rsplit('/', 1)[-1]
    main_category_dir = os.path.join('job_profil', main_category_name)
    os.makedirs(main_category_dir, exist_ok=True)

    for job in job_titles:
        job_name = job.text.strip()
        job_url_name = job_name.replace(' ', '-')
        job_url_name = job_url_name.replace("'", '')
        job_url_name = job_url_name.replace(",", '')
        job_url_name = job_url_name.replace("(", '')
        job_url_name = job_url_name.replace(")", '')
        job_dir_name = job_name.lower().replace(' ', '_')
        if job_url_name == "Clinical-scientist-cardiac-science":
            job_url_name = "Clinical-scientist-cardiac-sciences"

        job_dir = os.path.join(main_category_dir, job_dir_name)
        os.makedirs(job_dir, exist_ok=True)

        job_profile_url = f'https://www.prospects.ac.uk/job-profiles/{job_url_name}'
        print(job_profile_url)
        response = requests.get(job_profile_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        skills_section = soup.find('h2', id='skills').find_next_sibling('ul')
        skills = [li.get_text(strip=True) for li in skills_section.find_all('li')]

        skills_file_path = os.path.join(job_dir, 'skills.txt')
        with open(skills_file_path, 'w', encoding='utf-8') as file:
            for skill in skills:
                file.write(skill + '\n')

        responsibilities_section = soup.find('h2', id='responsibilities').find_next_sibling('ul')
        responsibilities = [li.get_text(strip=True) for li in responsibilities_section.find_all('li')]

        responsibilities_file_path = os.path.join(job_dir, 'responsibilities.txt')
        with open(responsibilities_file_path, 'w', encoding='utf-8') as file:
            for responsibility in responsibilities:
                file.write(responsibility + '\n')

