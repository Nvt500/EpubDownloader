import requests
from ebooklib import epub
from api import Novel, search


DOWNLOAD_PATH = "epubs/"


def make(novel: Novel, download_path: str = "") -> str:

    if not download_path:
        download_path = DOWNLOAD_PATH

    book = epub.EpubBook()

    book.set_identifier(f"{novel.title}{len(novel.chapters)}")
    book.set_title(novel.title)
    book.set_language("en")

    book.add_author(novel.author)

    book.set_cover("cover.jpg", requests.get(novel.cover_image, headers={"User-Agent": "Mozilla/5.0"}).content)

    cover = epub.EpubHtml(title="Cover", file_name="cover_page.xhtml")
    cover.content = "<img src=\"cover.jpg\" width=\"100%\" height=\"100%\">"
    book.add_item(cover)
    book.toc.append(cover)

    book.spine = ["cover", cover, "nav"]

    for index, chapter in enumerate(novel.chapters):
        c = epub.EpubHtml(title=chapter.title, file_name=f"{"_".join(chapter.title.split(" "))}{index}.xhtml")
        c.content = chapter.text
        book.add_item(c)
        book.toc.append(c)
        book.spine.append(c)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(f"{download_path}{"_".join(novel.title.split(" "))}.epub", book)

    return f"{download_path}{"_".join(novel.title.split(" "))}.epub"


"""
novel = search("readlightnovel", "supreme harem")[0]

novel.get_chapters(print_info=True)

make(novel)
"""
