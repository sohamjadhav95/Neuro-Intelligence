
import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com/s?k=baby+food"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
products = soup.find_all('div', class_='s-result-item')
for product in products:
    name_tag = product.find('span', class_='a-text-normal')
    if name_tag:
        name = name_tag.text.strip()
        if "baby food" in name.lower():
            print(name)