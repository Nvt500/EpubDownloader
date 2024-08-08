import api.readlightnovel as readlightnovel
import api.lightnovelpub as lightnovelpub
from api.objects import Chapter, Novel


providers = {
    "readlightnovel": readlightnovel,
    "lightnovelpub": lightnovelpub,
}


def get_chapter_info(provider: str, chapter: Chapter) -> tuple:

    if provider not in providers:
        raise ValueError("Provider must be one of: " + ", ".join(providers.keys()))

    return providers.get(provider).get_chapter_info(chapter)


def get_chapters(provider: str, novel: Novel) -> list[Chapter] | None:

    if provider not in providers:
        raise ValueError("Provider must be one of: " + ", ".join(providers.keys()))

    return providers.get(provider).get_chapters(novel)


def search(provider: str, query: str) -> list[Novel]:

    if provider not in providers:
        raise ValueError("Provider must be one of: " + ", ".join(providers.keys()))

    return providers.get(provider).search(query)
