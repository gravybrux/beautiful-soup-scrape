import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.coursereport.com/tracks/full-stack-developer'

response = requests.get(url)

if response.status_code == 200:
    
    page_content = response.content
    
    soup = BeautifulSoup(page_content, 'html.parser')
    
    list_items = soup.find_all('li', attrs={'data-ga': 'card'})
    
    data = []
    
    for li in list_items:
        h3 = li.find('h3', attrs={'data-ga': 'card-title'})
        
        a_elements = li.find_all('a', href=lambda value: value and value.startswith("/tracks/"))
        
        tracks = [a.text.strip() for a in a_elements]

        if h3:
            data.append({'name': h3.text.strip(), 'tracks': tracks})
    
    with open('data.json', 'w') as f:
        json.dump(data, f)
else:
    print('Failed to retrieve page')
