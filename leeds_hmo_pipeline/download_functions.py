import requests
from bs4 import BeautifulSoup
from io import BytesIO
import pandas as pd
from loguru import logger


def data_url(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        link_container = soup.find('div', class_='dstripe__body')
        
        if link_container:
            a_tag = link_container.find('a', href=True)
            if a_tag:
                href_value = a_tag['href']
                logger.info("URL found")
                return href_value
            else:
                logger.warning("Link not found.")
        else:
            logger.warning("Container not found.")
    else:
        logger.warning("Failed to fetch the URL:", url)
        

def load_excel_into_memory(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Use BytesIO to handle the binary content and read it into a pandas DataFrame
        # This loads the content into memory instead of creating a local file
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        
        logger.success("Excel file loaded into memory successfully.")
        return df
    else:
        logger.warning("Failed to load the Excel file.")
        return None