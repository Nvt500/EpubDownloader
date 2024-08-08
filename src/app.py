import api
import epub_maker
import os
from flask import Flask, render_template, request, session, send_file


app = Flask(__name__)

app.secret_key = b'890b51db46ed652bb62aecc5f4c2d5f64309cfa2a50afcd130bdb420837182a3'


@app.get("/")
def get_root():

    session.pop("novels", None)
    session.pop("novel", None)
    return render_template("search.html")


@app.get("/search")
def get_search():

    session.pop("novels", None)
    session.pop("novel", None)
    query = request.args.get("query", "")

    novels = api.search("readlightnovel", query)

    session["novels"] = [{
        "title": novel.title,
        "url": novel.url,
        "cover_image": novel.cover_image
    } for novel in novels]

    return render_template("results.html", novels=novels)


@app.get("/read")
def get_read():

    if os.listdir("static/downloads"):
        for file in os.listdir("static/downloads"):
            os.remove(os.path.join("static/downloads", file))

    title = request.args.get("novel-title", "")

    if title:
        if len(session["novels"]) == 1:
            novel = session["novels"][0]
        else:
            novel = [novel for novel in session["novels"] if novel["title"] == title][0]

        session.pop("novels", None)

        novel = api.Novel(novel["title"], novel["url"], novel["cover_image"], "", [], api.readlightnovel.get_chapters)

        novel.get_chapters(only_links=True)

        session["novel"] = {
            "title": novel.title,
            "url": novel.url,
            "cover_image": novel.cover_image,
            "author": novel.author,
            "chapters": [{
                "url": chapter.url
            } for chapter in novel.chapters]
        }

        novel.get_chapter(0)

        return render_template("read.html", novel=novel, index=0)

    chapter = int(request.args.get("chapter", ""))

    novel = api.Novel(session["novel"]["title"], session["novel"]["url"], session["novel"]["cover_image"], session["novel"]["author"], [api.Chapter("", chap["url"], "", api.readlightnovel.get_chapter_info) for chap in session["novel"]["chapters"]], api.readlightnovel.get_chapters)

    novel.get_chapter(chapter)

    return render_template("read.html", novel=novel, index=chapter)


@app.get("/download")
def get_download():

    novel = api.Novel(session["novel"]["title"], session["novel"]["url"], session["novel"]["cover_image"], session["novel"]["author"], [], api.readlightnovel.get_chapters)

    novel.get_chapters()

    path = epub_maker.make(novel, download_path="static/downloads/")

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run()
