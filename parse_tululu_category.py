import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_book_urls_from_category_url(category_url, start_page, end_page):
    book_urls = []
    for page in range(start_page, end_page + 1):
        url = f'{category_url}{page}/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.select('table.d_book')
        for book in books:
            book_url = urljoin('http://tululu.org/', book.select_one('a')['href'])
            book_urls.append(book_url)
    return book_urls
