from __future__ import annotations
import concurrent.futures
from dataclasses import dataclass
from typing import Callable


MAX_WORKERS = 30


@dataclass
class Chapter:
    title: str
    url: str
    text: str
    func: Callable

    def __repr__(self) -> str:
        return f"{self.title}: {self.url}"

    def get_info(self) -> None:
        self.title, self.text = self.func(self)


@dataclass
class Novel:
    title: str
    url: str
    cover_image: str
    author: str
    chapters: list[Chapter]
    func: Callable

    def __repr__(self) -> str:

        return f"{self.title} by {self.author}"

    def get_chapters(self, only_links: bool = False, print_info: bool = False, max_workers: int = 0) -> None:

        self.chapters = self.func(self)

        if only_links:
            return

        if not max_workers:
            max_workers = MAX_WORKERS

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(chapter.get_info): chapter for chapter in self.chapters}
            for future in concurrent.futures.as_completed(future_to_url):
                chapter = future_to_url.get(future)
                try:
                    future.result()
                except Exception as e:
                    if print_info:
                        print(f"Error {str(e)}: {chapter.url}")
                else:
                    if print_info:
                        print(f"Done: {chapter.url}")

    def get_chapter(self, index: int) -> None:

        self.chapters[index].get_info()

    def get_num_done_chapters(self) -> int:

        num = 0
        for chapter in self.chapters:
            if chapter.text != "":
                num += 1

        return num

    def chapters_have_data(self) -> bool:

        for chapter in self.chapters:
            if not chapter.title:
                return False

        return True

    def convert_chapters_for_js(self) -> Novel:

        new_novel = Novel(self.title, self.url, self.cover_image, self.author, [], self.func)

        for chapter in self.chapters:
            text = chapter.text.split("\"")
            text = "\\\"".join(text)
            text = text.split("\'")
            text = "\\\'".join(text)
            text = text.split("\n")
            text = "\\\n".join(text)
            new_novel.chapters.append(Chapter(chapter.title, chapter.url, text, chapter.func))

        return new_novel
