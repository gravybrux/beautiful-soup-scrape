import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

base_url = 'https://www.coursereport.com'
url_path = '/tracks/full-stack-developer'
url = urljoin(base_url, url_path)

response = requests.get(url)

if response.status_code == 200:
    
    page_content = response.content
    
    soup = BeautifulSoup(page_content, 'html.parser')
    
    list_items = soup.find_all('li', attrs={'data-ga': 'card'})
    
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

        page_link_response = requests.get(page_link)

        if page_link_response.status_code == 200:
            page_link_content = page_link_response.content

            page_link_soup = BeautifulSoup(page_link_content, 'html.parser')

            h3_elements = page_link_soup.find_all('h3', attrs={'data-ga': 'card-title'})

            courses = [{'course_name': h3.text.strip()} for h3 in h3_elements]
        else:
            courses = []

        data.append({'name': h3.text.strip(), 'description': description, 'tracks': tracks, 'page_link': page_link, 'courses': courses})
    
    with open('data.json', 'w') as f:
        json.dump(data, f)
else:
    print('Failed to retrieve page')
