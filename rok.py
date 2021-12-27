import requests
from bs4 import BeautifulSoup


def get_job_data(URL):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    result = requests.get(URL, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    data = soup.find('div', class_='page').find_all('tr', class_='job')

    return data


def extract_job(data):
    title = data.find('h2').get_text(strip=True)
    company = data.find('h3').get_text(strip=True)
    link = data['data-url']

    return {
        'title': title,
        'company': company,
        'link': f'https://remoteok.com{link}'
    }


def extract_jobs(job_data):
    jobs = []

    for data in job_data:
        print(f'Scrapping ROK')
        job = extract_job(data)
        jobs.append(job)

    return jobs


def get_jobs(word):
    URL = f"https://remoteok.io/remote-dev+{word}-jobs"

    job_data = get_job_data(URL)
    jobs = extract_jobs(job_data)

    return jobs
