import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import bs4
import requests

HEADERS = {'user-agent': 'Mozilla/5.0'}


def get_chapter(chapter_url):
    chapter, url = chapter_url
    r = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(r.content, 'lxml', parse_only=bs4.SoupStrainer('div', id='chapter-content'))
    paragraphs = [p.text for p in soup('p')]
    res = [chapter] + paragraphs
    print(chapter)
    return '\n\n'.join(res)


def get_novel(novel_name):
    url = f'https://www.wuxiaworld.com/novel/{novel_name}'
    r = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(r.content, 'lxml', parse_only=bs4.SoupStrainer('a'))
    chapters_urls = [(a.text.strip(), urljoin(url, a['href']))
                     for a in soup(href=re.compile(novel_name))]
    with ThreadPoolExecutor(max_workers=100) as pool:
        all_chapters = pool.map(get_chapter, chapters_urls)
    return '\n\n\n\n'.join(all_chapters)


if __name__ == '__main__':
    novel = 'fields-of-gold'
    novel_text = get_novel(novel)
    with open(f'{novel}.txt', 'w', encoding="utf-8") as f:
        f.write(novel_text)