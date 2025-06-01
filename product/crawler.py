import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import time
import re

FLIPKART_SOURCE_URL = 'https://www.flipkart.com'
AMAZON_SOURCE_URL = 'https://www.amazon.com'

class SearchCrawler(ABC):
    def __init__(self, query):
        self.query = query

    @abstractmethod
    def crawl(self, url):
        pass

class FlipkartCrawler(SearchCrawler):
    def __init__(self, query):
        super().__init__(query)
        self.source = 'flipkart'
        self.source_url = FLIPKART_SOURCE_URL
        self.url = f'{self.source_url}/search?q={self.query}'
        self.max_page_number = 2

    def crawl(self, url):
        response = requests.get(url)
        return response.text
    
    def crawl_multiple_pages(self):
        page_number = 1
        multiple_pages = []
        while page_number <= self.max_page_number:
            url = f'{self.url}&page={page_number}'
            print(f'crawling url: {url}')
            html = self.crawl(url)
            if html:
                multiple_pages.append(html)
            else:
                break
            page_number += 1
            time.sleep(2)
        return multiple_pages
    
class AmazonCrawler(SearchCrawler):
    def __init__(self, query):
        super().__init__(query)
        self.source = 'amazon'
        self.source_url = AMAZON_SOURCE_URL
        self.url = f'{self.source_url}/s?k={self.query}'

    def crawl(self, url):
        response = requests.get(url)
        return response.text

class Crawler:
    def __init__(self, query):
        self.query = query
        self.sources = {
            'flipkart': FlipkartCrawler,
            # 'amazon': AmazonCrawler
        }
        self.html_parsers = {
            'flipkart': FlipkartHTMLParser,
            # 'amazon': AmazonHTMLParser
        }

    def crawl(self):
        response = {source: [] for source in self.sources}
        for source in self.sources:
            multiple_pages = self.sources[source](self.query).crawl_multiple_pages()
            print(f'multiple_pages: {len(multiple_pages)}')

            for html_page in multiple_pages:
                product_links = self.html_parsers[source].extract_product_links(html_page)
                print(f'product_links: {len(product_links)}')
                for i, link in enumerate(product_links):
                    print(f'link: {link}')
                    product_details = self.html_parsers[source].extract_product_details(link)
                    if product_details['title'] and product_details['price'] and product_details['seller_name']:
                        response[source].append(product_details)
                    time.sleep(1)
                    
        return response


class HTMLParser(ABC):

    @staticmethod
    @abstractmethod
    def extract_product_links(html_page):
        pass

    @staticmethod
    @abstractmethod
    def extract_product_details(link):
        pass

class FlipkartHTMLParser(HTMLParser):
    @staticmethod
    def extract_product_links(html_page):
        soup = BeautifulSoup(html_page, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', class_='CGtC98', href=True):
            href = a_tag['href']
            if href.startswith('/'):
                href = FLIPKART_SOURCE_URL + href.split('?')[0]
                links.append(href)
        return links
    
    @staticmethod
    def extract_product_details(link):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        return {
            'title': FlipkartHTMLParser.extract_title(soup),
            'price': FlipkartHTMLParser.extract_price(soup),
            'rating': FlipkartHTMLParser.extract_rating(soup),
            'number_of_reviews': FlipkartHTMLParser.extract_number_of_reviews(soup),
            'seller_name': FlipkartHTMLParser.extract_seller_name(soup),
            'link': link,
            'source': 'flipkart'
        }
    
    @staticmethod
    def extract_number_of_reviews(soup):
        if soup.find('span', class_='Wphh3N'):
            rating_text = soup.find('span', class_='Wphh3N').get_text(separator=' ', strip=True)
            rating = re.search(r'\b\d[\d,]*\s+Reviews\b', rating_text).group(0)
            return int(rating.split(' ')[0].replace(',', '')) if rating else None
        else:
            return None
    
    @staticmethod
    def extract_price(soup):
        if soup.find('div', class_='Nx9bqj CxhGGd'):
            amount_text = soup.find('div', class_='Nx9bqj CxhGGd').text
            amount = re.search(r'\d+(,\d+)*', amount_text)
            if amount:
                return int(amount.group(0).replace(',', ''))
            else:
                return None
        else:
            return None
    
    @staticmethod
    def extract_title(soup):
        if soup.find('span', class_='VU-ZEz'):
            return soup.find('span', class_='VU-ZEz').text
        else:
            return None
    
    @staticmethod
    def extract_rating(soup):
        if soup.find('div', class_='XQDdHH'):
            rating_text = soup.find('div', class_='XQDdHH').text
            rating = re.search(r'\d(\.\d)?', rating_text)
            if rating:
                return rating.group(0)
            else:
                return None
        else:
            return None
    
    @staticmethod
    def extract_seller_name(soup):
        if soup.find('div', id='sellerName'):
            return soup.find('div', id='sellerName').find('span').find('span').text
        else:
            return None
    
class HTMLParserFactory:
    @staticmethod
    def get_html_parser(source):
        if source == 'flipkart':
            return FlipkartHTMLParser
        else:
            return None

# class AmazonHTMLParser(HTMLParser):
#     @staticmethod
#     def extract_product_links(html_page):
#         soup = BeautifulSoup(html_page, 'html.parser')
#         links = []
#         for a_tag in soup.find_all('a', href=True):
#             links.append(a_tag['href'])
#         return links

#     @staticmethod
#     def extract_product_details(link):
#         response = requests.get(link)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         return {
#             'title': AmazonHTMLParser.extract_title(soup),
#             'price': AmazonHTMLParser.extract_price(soup),
#             'rating': AmazonHTMLParser.extract_rating(soup),
#             'number_of_reviews': AmazonHTMLParser.extract_number_of_reviews(soup),
#             'seller_name': AmazonHTMLParser.extract_seller_name(soup),
#             'link': link,
#             'source': 'amazon'
#         }
    
#     @staticmethod
#     def extract_number_of_reviews(soup):
#         if soup.find('span', class_='Wphh3N'):
#             rating_text = soup.find('span', class_='Wphh3N').get_text(separator=' ', strip=True)
#             rating = re.search(r'\b\d[\d,]*\s+Reviews\b', rating_text).group(0)
#             return int(rating.split(' ')[0].replace(',', '')) if rating else None
#         else:
#             return None
    
#     @staticmethod
#     def extract_price(soup):
#         if soup.find('span', class_='Nx9bqj CxhGGd'):
#             amount_text = soup.find('span', class_='Nx9bqj CxhGGd').text
#             amount = re.search(r'\d+(,\d+)*', amount_text)
#             if amount:
#                 return int(amount.group(0).replace(',', ''))
#             else:
#                 return None
#         else:
#             return None
    
#     @staticmethod
#     def extract_title(soup):
#         if soup.find('span', class_='Nx9bqj CxhGGd'):
#             return soup.find('span', class_='Nx9bqj CxhGGd').text
#         else:
#             return None
    