import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import concurrent.futures

base_url = 'https://www.coursereport.com'
url_path = '/tracks/full-stack-developer'
url = urljoin(base_url, url_path)


def get_page_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.content
    else:
        print('Failed to retrieve page')
        return None


def extract_courses(url):
    page_content = get_page_content(url)
    
    if not page_content:
        return []
    
    soup = BeautifulSoup(page_content, 'html.parser')

    h2_elements = soup.find_all('h2', id='courses')

    courses = [{'course_name': h2.text.strip()} for h2 in h2_elements]

    return courses


def extract_list_items():
    page_content = get_page_content(url)
    
    if not page_content:
        return []
    
    soup = BeautifulSoup(page_content, 'html.parser')

    list_items = soup.find_all('li', attrs={'data-ga': 'card'})

    return list_items


def extract_data():
    list_items = extract_list_items()

    data = []

    for li in list_items:
        h3 = li.find('h3', attrs={'data-ga': 'card-title'})

        if not h3:
            continue

        a_parent = h3.find_parent('a')

        if not a_parent:
            continue

        page_link = urljoin(base_url, a_parent.get('href'))

        description_div = li.find('div', class_='hidden md:block')

        a_elements = li.find_all('a', href=lambda value: value and value.startswith("/tracks/"))

        tracks = [a.text.strip() for a in a_elements]

        description = description_div.text.strip() if description_div else ""

        data.append({'name': h3.text.strip(), 'description': description, 'tracks': tracks, 'page_link': page_link})

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for item, courses in zip(data, executor.map(extract_courses, [item['page_link'] for item in data])):
            item['courses'] = courses

    return data


def write_to_file(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


def main():
    data = extract_data()
    write_to_file(data)


if __name__ == "__main__":
    main()
