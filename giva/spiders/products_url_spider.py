import gzip
import hashlib
import os
from typing import Iterable

import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from giva.items import ProductRawItem


def ensure_dir_exists(dir_path: str):
    # Check if the specified directory exists, and create it if it doesn't
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


# Define the project name and construct the directory path for project files
project_name = 'giva'
project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
ensure_dir_exists(dir_path=project_files_dir)  # Ensure the project files directory exists


class ProductsUrlSpiderSpider(scrapy.Spider):
    name = "products_url_spider"  # Name of the spider

    # allowed_domains = ["xyz.com"]  # Define allowed domains (currently commented out)

    def __init__(self):
        super().__init__()

        # Connect to the MySQL database
        self.client = pymysql.Connect(
            database='giva_db',
            user='root',
            password='actowiz',
            autocommit=True,  # Enable autocommit mode
        )
        self.cursor = self.client.cursor()  # Create a cursor object to interact with the database

    def start_requests(self) -> Iterable[Request]:
        # Define the initial URL to start scraping
        start_url = "https://www.giva.co/collections/all"
        # C:/Users/jaimin.gurjar/AppData/Local/Temp/Rar$EXa5156.7368.rartemp/{}.html
        print('Working on:', start_url)  # Print the URL being processed
        yield scrapy.Request(
            url=start_url,
            method='GET',  # Use GET method to request the page
            callback=self.parse  # Specify the callback method to handle the response
        )

    def parse(self, response):
        # Extract and print the response URL and HTTP status code
        response_url = response.url
        print('Response Url:', response_url)
        status_code = response.status
        print('HTTP STATUS CODE:', status_code)

        response_text = response.body
        # Saving Page
        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)

        file_path = os.path.join(project_files_dir, 'All_Collection_Pages', filename)
        ensure_dir_exists(os.path.dirname(file_path))  # Ensure the 'Product_Pages' directory exists
        with gzip.open(file_path, mode='wb') as file:
            file.write(response_text)
            print('Page Saved')

        # script_text = response.xpath('//script[@type="application/ld+json" and contains(text(), "ItemList")]/text()').get()
        # json_script = json.loads(script_text)
        # print(type(json_script))
        # print(json_script)
        products_names_list = response.xpath('//ul[@id="product-grid"]/li//h3[@class="card__heading"]/a/text()').getall()
        product_urls_list = response.xpath('//ul[@id="product-grid"]/li//h3[@class="card__heading"]/a/@href').getall()
        for product_name, product_url_slug in zip(products_names_list, product_urls_list):
            product_name = product_name.replace('\n', '').strip()
            product_url = 'https://www.giva.co' + product_url_slug
            print('Product Name:', product_name)
            print('Product URL:', product_url)
            product_raw_item = ProductRawItem()
            product_raw_item['product_name'] = product_name
            product_raw_item['product_url'] = product_url

            yield product_raw_item
            print('*' * 50)
        print('\n\n\n')
        print('-' * 100)

        # Find the next page URL using XPath and follow it if it exists
        next_page_url = response.xpath('//link[@rel="next"]/@href').get()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse)  # Follow the next page link


if __name__ == '__main__':
    # Execute the spider
    execute(f'scrapy crawl {ProductsUrlSpiderSpider.name}'.split())
