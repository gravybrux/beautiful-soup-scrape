import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# Base URL of the page
base_url = 'https://www.coursereport.com'
# Path of the page
url_path = '/tracks/full-stack-developer'
# Full URL of the page
url = urljoin(base_url, url_path)

# Send GET request to the page
response = requests.get(url)

# If the GET request is successful, the status code will be 200
if response.status_code == 200:
    
    # Get the content of the response
    page_content = response.content
    
    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Find all 'li' elements with 'data-ga' attribute equals 'card'
    list_items = soup.find_all('li', attrs={'data-ga': 'card'})
    
    # Create a list to hold the data
    data = []
    
    # Loop through the list items
    for li in list_items:
        # Find the 'h3' child with 'data-ga' attribute equals 'card-title'
        h3 = li.find('h3', attrs={'data-ga': 'card-title'})
        
        # If 'h3' child is not found, skip this iteration
        if not h3:
            continue

        # Find the parent 'a' element of 'h3'
        a_parent = h3.find_parent('a')

        # If parent 'a' is not found, skip this iteration
        if not a_parent:
            continue
        
        # Extract the 'href' from the 'a' tag and combine it with the base url
        page_link = urljoin(base_url, a_parent.get('href'))

        # Find the first 'div' element with class attribute containing 'hidden md:block'
        description_div = li.find('div', class_='hidden md:block')

        # Find 'a' elements with 'href' attribute starting with "/tracks/"
        a_elements = li.find_all('a', href=lambda value: value and value.startswith("/tracks/"))

        # Get the text of 'a' elements
        tracks = [a.text.strip() for a in a_elements]

        # If description div is found, get its text
        description = description_div.text.strip() if description_div else ""

        # Add the data to the list
        data.append({'name': h3.text.strip(), 'description': description, 'tracks': tracks, 'page_link': page_link})
    
    # Write data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f)
else:
    print('Failed to retrieve page')
