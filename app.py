import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from io import BytesIO
from pytubefix.exceptions import PytubeFixError
from pathlib import Path

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    send_file,
)

app = Flask(__name__)


@app.route("/")
def index():
    print("Request for index page received")
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/hello", methods=["POST"])
def hello():
    url = request.form.get("name")
    path = request.form.get("path")
    try:
        audio(url, path)
    except PytubeFixError:
        print("error")

    return render_template('hello.html', name = path)

def audio(thelink, path):
    try:
        yt = YouTube(thelink)
        print('Title:', yt.title)
        print('Views:', yt.views)
        video = yt.streams.filter(abr='160kbps', only_audio=True).last()
        out_file = video.download(output_path=path)
        base, ext = os.path.splitext(out_file)
        new_file = Path(f'{base}.mp3')
        os.rename(out_file, new_file)
        if new_file.exists():
            print(f'{yt.title} has been successfully downloaded.')
    except Exception as e:
        print(f'ERROR: {yt.title}could not be downloaded! \n Error: {e}')

if __name__ == "__main__":
    app.run()