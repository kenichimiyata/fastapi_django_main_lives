import requests
from bs4 import BeautifulSoup
import openpyxl
import schedule
import time

class Scraper:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file

    def scrape(self):
        # Send request to the website
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product data
        products = []
        for product in soup.find_all('div', {'class': 'product'}):
            name = product.find('h2', {'class': 'product-name'}).text.strip()
            price = product.find('span', {'class': 'price'}).text.strip()
            products.append({'name': name, 'price': price})

        # Save data to xlsx file
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Name', 'Price'])
        for product in products:
            ws.append([product['name'], product['price']])
        wb.save(self.output_file)

def daily_scrape():
    scraper = Scraper('https://example.com', 'output.xlsx')
    scraper.scrape()

schedule.every(1).day.at("00:00").do(daily_scrape)  # Run daily at midnight

while True:
    schedule.run_pending()
    time.sleep(1)