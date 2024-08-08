import requests
from bs4 import BeautifulSoup
from random import choice
from api.user_agents import USER_AGENTS
from api.objects import Chapter, Novel


BASE_URL = "https://www.readlightnovel.meme/"

SEARCH_URL = "https://www.readlightnovel.meme/search/autocomplete"


def get_chapter_info(chapter: Chapter) -> tuple:

    while True:
        try:
            response = requests.get(chapter.url, headers={
                "User-Agent": choice(USER_AGENTS)
            })
            break
        except Exception:
            pass

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("a", attrs={"class": "black-link"}).parent.text.strip()

    soup = soup.find("div", attrs={"id": "growfoodsmart"})

    return title, soup.prettify()


def get_chapters(novel: Novel) -> list[Chapter] | None:

    while True:
        try:
            response = requests.get(novel.url, headers={
                "User-Agent": choice(USER_AGENTS)
            })
            break
        except Exception:
            pass

    soup = BeautifulSoup(response.text, "html.parser")

    div = soup.find("div", attrs={"class": "novel"})

    for item in div.find("div", attrs={"class": "novel-left"}).find("div", attrs={"class": "novel-details"}):
        try:
            if item.div.h3.text == "Author(s)":
                for i in item.children:
                    try:
                        novel.author = i.ul.text.strip()
                    except AttributeError:
                        continue
        except AttributeError:
            continue

    uls = soup.find_all("ul", {"class": "chapter-chs"})

    if not uls:
        return None

    links = []
    for ul in uls:
        for li in ul.children:
            if li.name == "li":
                links.append(li.a.get("href"))

    return [Chapter("", link, "", get_chapter_info) for link in links]


def search(query: str) -> list[Novel]:

    payload = {
        "q": query
    }

    while True:
        try:
            response = requests.post(SEARCH_URL, data=payload, headers={
                "User-Agent": choice(USER_AGENTS),
                "X-Requested-With": "XMLHttpRequest"
            })
            break
        except Exception:
            pass

    soup = BeautifulSoup(response.text, "html.parser")

    novels = []
    for a in soup.find_all("a"):
        url = a.get("href")
        cover_image = a.span.img.get("src")
        title = a.span.next_sibling.text
        novels.append(Novel(title, url, cover_image, "", [], get_chapters))

    return novels
