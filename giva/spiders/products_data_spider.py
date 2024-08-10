import gzip
import hashlib
import json
import os
from typing import Iterable
import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from giva.items import ProductDataItem
import re


def remove_html_tags(text):
    """
    Removes HTML tags from a string using a regular expression.
    :param text: The input string containing HTML tags.
    :return: The cleaned string with HTML tags removed.
    """
    clean_pattern = re.compile('<.*?>')
    cleaned_text = re.sub(clean_pattern, '', text)
    return cleaned_text


def ensure_dir_exists(dir_path: str):
    """
    Ensures that the specified directory exists. If it doesn't, the directory is created.
    :param dir_path: The path of the directory to check or create.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Confirm directory creation


# Define the project name and construct the directory path for project files
project_name = 'giva'
project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
ensure_dir_exists(dir_path=project_files_dir)  # Ensure the project files directory exists


def get_product_name(json_dict):
    """
    Extracts the 'name' field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product name or 'N/A' if the field is not present.
    """
    return json_dict.get('name', 'N/A')


def get_product_url(json_dict):
    """
    Extracts the 'url' field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product URL or 'N/A' if the field is not present.
    """
    return json_dict.get('url', 'N/A')


def get_product_image_url(json_dict):
    """
    Extracts the 'image' field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product image URL or 'N/A' if the field is not present.
    """
    return json_dict.get('image', 'N/A')


def get_product_description(json_dict):
    """
    Extracts the 'description' field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product description or 'N/A' if the field is not present.
    """
    return json_dict.get('description', 'N/A')


def get_product_sku(json_dict):
    """
    Extracts the 'sku' field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product SKU or 'N/A' if the field is not present.
    """
    return json_dict.get('sku', 'N/A')


def get_product_brand(json_dict):
    """
    Extracts the 'brand' field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The brand name or 'N/A' if the field is not present.
    """
    return json_dict.get('brand', {}).get('name', 'N/A')


def get_product_offer_price(json_dict):
    """
    Extracts the 'offers' price field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product offer price or 'N/A' if the field is not present.
    """
    return json_dict.get('offers', {})[0].get('price', 'N/A')


def get_product_currency(json_dict):
    """
    Extracts the 'offers' currency field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product currency or 'N/A' if the field is not present.
    """
    return json_dict.get('offers', {})[0].get('priceCurrency', 'N/A')


def get_product_variant_url(json_dict):
    """
    Extracts the 'offers' variant URL field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product variant URL or 'N/A' if the field is not present.
    """
    return json_dict.get('offers', {})[0].get('url', 'N/A')


def get_product_rating_value(json_dict):
    """
    Extracts the 'aggregateRating' value field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product rating value or 'N/A' if the field is not present.
    """
    return json_dict.get('aggregateRating', {}).get('ratingValue', 'N/A')


def get_product_review_count(json_dict):
    """
    Extracts the 'aggregateRating' review count field from the JSON dictionary if it exists.
    :param json_dict: The JSON dictionary containing product data.
    :return: The product review count or 'N/A' if the field is not present.
    """
    return json_dict.get('aggregateRating', {}).get('reviewCount', 'N/A')


def get_shipping_data(response):
    shipping_data_list = response.xpath('//div[@class="accordion__content"]/ul/li/text()').getall()
    shipping_data = ' '.join(shipping_data_list)
    return shipping_data


class ProductsDataSpiderSpider(scrapy.Spider):
    name = "products_data_spider"

    def __init__(self):
        super().__init__()

        # Connect to the MySQL database
        self.client = pymysql.Connect(
            database='giva_db',
            user='root',
            password='actowiz',
            autocommit=True  # Enable autocommit mode
        )
        self.cursor = self.client.cursor()  # Create a cursor object to interact with the database

        # Path to the file where URLs with non-200 status codes will be saved
        self.error_log_file = os.path.join(project_files_dir, 'Error_Urls',  'error_urls.txt')

    def log_error_url(self, url: str, status_code: int):
        """
        Logs the URLs that return non-200 status codes into a text file.
        :param url: The URL that returned a non-200 status code.
        :param status_code: The HTTP status code returned.
        """
        with open(self.error_log_file, 'a') as f:
            f.write(f'{url} - Status Code: {status_code}\n')
        print(f'Logged error URL: {url} with status code {status_code}')

    def start_requests(self) -> Iterable[Request]:
        """
        This method sends the initial requests to start the scraping process.
        It fetches URLs from the MySQL database and sends HTTP requests for each URL.
        """
        fetch_table = 'products_links'
        # Query to select URLs that are pending for scraping
        fetch_query = f'''SELECT * FROM {fetch_table} WHERE url_status = 'Pending' and id between 2401 and 2810;'''
        self.cursor.execute(query=fetch_query)
        rows = self.cursor.fetchall()
        print(f'Fetched {len(rows)} data.')

        for row in rows:
            product_url = row[2]  # Assuming the URL is in the third column
            print('Working on:', product_url)
            # Yield a new request for each URL, which Scrapy will process asynchronously
            yield scrapy.Request(
                url=product_url,
                method='GET',
                callback=self.parse  # The parse method will handle the response
            )

    def parse(self, response):
        """
        This method processes the HTTP response for each product URL.
        It saves the response content and extracts product data from the JSON-LD script.
        """
        # Extract and print the response URL and HTTP status code
        response_url = response.url
        print('Response Url:', response_url)
        status_code = response.status
        print('HTTP STATUS CODE:', status_code)

        # Check if the response status code is not 200
        if status_code != 200:
            print(status_code)
            self.log_error_url(url=response_url, status_code=status_code)
            return  # Skip further processing for this URL

        response_text = response.body
        # Generate a filename using a hash of the URL and save the response content
        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)

        # Construct the file path and ensure the directory exists
        file_path = os.path.join(project_files_dir, 'Products_Pages', filename)
        ensure_dir_exists(os.path.dirname(file_path))
        # Save the response content as a gzipped HTML file
        with gzip.open(file_path, mode='wb') as file:
            file.write(response_text)
            print('Page Saved')

        # Extract the JSON-LD script from the page and parse it
        json_text = response.xpath('''//script[@type="application/ld+json" and contains(text(), '"@type": "Product"')]/text()''').get()
        json_dict = json.loads(json_text.replace('\n', '').replace(r'\/', '/'))
        # print('JSON DICT>>>', json_dict)

        # Create a new instance of the ProductDataItem to store extracted data
        product_data_item = ProductDataItem()

        # Extract product information using helper functions and store in the item
        product_data_item['product_name'] = get_product_name(json_dict)
        product_data_item['product_url'] = get_product_url(json_dict)
        product_data_item['product_image_url'] = get_product_image_url(json_dict)
        product_data_item['product_description'] = get_product_description(json_dict)
        product_sku = get_product_sku(json_dict)
        product_data_item['product_sku'] = product_sku
        product_data_item['product_brand'] = get_product_brand(json_dict)
        product_data_item['product_offer_price'] = get_product_offer_price(json_dict)
        product_data_item['product_currency'] = get_product_currency(json_dict)
        product_data_item['product_variant_url'] = get_product_variant_url(json_dict)
        product_data_item['product_rating_value'] = get_product_rating_value(json_dict)
        product_data_item['product_review_count'] = get_product_review_count(json_dict)
        product_data_item['shipping_data'] = get_shipping_data(response)

        # List of pincodes to check delivery times
        pincode_list = ['560001', '400001', '700020', '110001']
        for pincode in pincode_list:
            # Construct the delivery time API URL
            delivery_time_url = f'https://api.giva.co/getDeliveryTime?pin={pincode}&sku={product_sku}'
            # Yield a new request to check delivery times for each pincode
            delivery_time_request = scrapy.Request(
                url=delivery_time_url,
                callback=self.parse_delivery_time,
                meta={'product_data_item': product_data_item,
                      'pincode': pincode
                      }
            )
            # print('product url...', response_url)
            yield delivery_time_request
            # print('SENDING PINCODE...', pincode)

    def parse_delivery_time(self, response):
        """
        This method processes the response from the delivery time API.
        It saves the response content and extracts the delivery time message.
        """
        # Extract and print the response URL and HTTP status code
        response_url = response.url
        print('Response Url:', response_url)
        status_code = response.status
        print('HTTP STATUS CODE:', status_code)

        # Retrieve the product data item and pincode from the response meta
        product_data_item = response.meta['product_data_item']
        pincode = response.meta['pincode']
        # print(product_data_item)
        # print(pincode)

        response_text = response.body
        # Generate a filename using a hash of the URL and save the response content
        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        filename = product_data_item['product_sku'] + ' _ ' + pincode + '.html.gz'
        print('Filename is:', filename)

        # Construct the file path and ensure the directory exists
        file_path = os.path.join(project_files_dir, 'Delivery_Time_Pages', filename)
        ensure_dir_exists(os.path.dirname(file_path))
        # Save the response content as a gzipped HTML file
        with gzip.open(file_path, mode='wb') as file:
            file.write(response_text)
            print('Page Saved')

        # Parse the JSON response from the delivery time API
        response_text = response.body.decode()
        json_data = json.loads(response_text)
        message_with_tags = json_data['message']
        # Remove HTML tags from the delivery time message
        delivery_time_message = remove_html_tags(text=message_with_tags)
        # print(delivery_time_message)
        # Store the delivery time message and pincode in the product data item
        product_data_item['pincode'] = pincode
        product_data_item['delivery_time_message'] = delivery_time_message
        # Yield the final product data item
        yield product_data_item
        print('+' * 25)


if __name__ == '__main__':
    # Execute the spider
    execute(f'scrapy crawl {ProductsDataSpiderSpider.name}'.split())
