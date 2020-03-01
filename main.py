import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from parse_tululu_category import get_book_urls_from_category_url
import json
import argparse
from dotenv import load_dotenv

FANTASTIC_CATEGORY_URL = 'http://tululu.org/l55/'


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', default=1, type=int)
    parser.add_argument('--end_page', default=701, type=int)
    return parser


def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    filepath = os.path.join(folder, sanitize_filename(filename) + '.txt')
    with open(filepath, 'w', encoding='utf8') as file:
        file.write(response.text)
    return filepath


def download_image(url, filename, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    filepath = os.path.join(folder, sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_title_and_author_from_soup(soup):
    title_tag = soup.select_one('head title')
    title_text = title_tag.text
    title_text_split = title_text.split(' - ')
    title = title_text_split[0].strip()
    author = title_text_split[1].split(',')[0].strip()
    return title, author


def get_comments_from_soup(soup):
    comments_tags = soup.select('div.texts span')
    comments = [comment_tag.text for comment_tag in comments_tags]
    return comments


def get_genres_from_soup(soup):
    genre_tags = soup.select('span.d_book a')
    genres = [genre_tag.text for genre_tag in genre_tags]
    return genres


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    books = []
    try:
        book_urls = get_book_urls_from_category_url(FANTASTIC_CATEGORY_URL, args.start_page, args.end_page)
    except requests.exceptions.HTTPError as err:
        print(err)
        exit(-1)
    for book_url in book_urls:
        response = requests.get(book_url, allow_redirects=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        title, author = get_title_and_author_from_soup(soup)
        comments = get_comments_from_soup(soup)
        genres = get_genres_from_soup(soup)
        image_url = urljoin('http://tululu.org/', soup.select_one('div.bookimage img')['src'])
        book_id = book_url.strip('/').split('/')[-1].strip('b')
        txt_url = f'http://tululu.org/txt.php?id={book_id}'
        book_path = download_txt(txt_url, title)
        image_src = download_image(image_url, image_url.split('/')[-1])
        book = {
                'title': title,
                'author': author,
                'image_src': image_src,
                'book_path': book_path,
                'comments': comments,
                'genres': genres,
            }
        books.append(book)

    load_dotenv()
    file_name = os.getenv('BOOK_INFORMATION_FILE_NAME')
    with open(file_name, "w", encoding='utf8') as my_file:
        json.dump(books, my_file, sort_keys=True, indent=4, ensure_ascii=False)
