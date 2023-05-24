import requests
from bs4 import BeautifulSoup
import json

# URL of the page
url = 'https://www.coursereport.com/tracks/full-stack-developer'

# Send GET request to the page
response = requests.get(url)

# If the GET request is successful, the status code will be 200
if response.status_code == 200:
    
    # Get the content of the response
    page_content = response.content
    
    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Find all divs with 'data-ga' attribute equals 'card-title'
    divs = soup.find_all('h3', attrs={'data-ga': 'card-title'})
    
    # Create a list to hold the data
    data = []
    
    # Loop through the divs and get the text inside the div
    for div in divs:
        data.append({'name': div.text.strip()})
    
    # Write data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f)
else:
    print('Failed to retrieve page')
