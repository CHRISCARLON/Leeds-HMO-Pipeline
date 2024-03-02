import requests
from bs4 import BeautifulSoup
from loguru import logger

def find_the_date(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the element based on class names (adjust selectors as needed)
        # We are looking for the file name from the class below
        date_element = soup.find('span', class_='has-text-weight-bold has-text-link untrusted')
        if date_element:
            date_text = date_element.get_text()
            return date_text
        else:
            logger.warning("Date element not found.")
    else:
        logger.warning(f"Failed to retrieve the webpage. Status code: {response.status_code}")