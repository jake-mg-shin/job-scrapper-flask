import requests
from bs4 import BeautifulSoup


def get_all_url(URL):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    urls = soup.find_all('li', class_='view-all')

    all_urls = []

    for url in urls:
        url = url.find('a')['href']
        all_urls.append(url)

    return all_urls


def get_all_link(get_urls):
    urls = get_urls
    all_links = []

    for url in urls:
        all_links.append(f'https://weworkremotely.com{url}')

    return all_links


def extract_job(each_data):
    data = each_data
    title = data.find('span', class_='title').get_text(strip=True)
    company = data.find('span', class_='company').get_text(strip=True)
    link = data.find('a', recursive=False)['href']

    return {
        'title': title,
        'company': company,
        'link': f'https://weworkremotely.com{link}'
    }


def extract_jobs(get_links):
    links = get_links

    jobs = []

    for link in links:
        print(f'Scrapping WWR')
        result = requests.get(link)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('section', class_='jobs')

        for result in results:
            data = result.find_all('li', class_='feature')

            for each_data in data:
                job = extract_job(each_data)
                jobs.append(job)

    return jobs


def get_jobs(word):
    URL = f"https://weworkremotely.com/remote-jobs/search?term={word}"

    get_urls = get_all_url(URL)
    get_links = get_all_link(get_urls)
    jobs = extract_jobs(get_links)

    return jobs
