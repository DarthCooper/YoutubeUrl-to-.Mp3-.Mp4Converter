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
    if path.strip() == "":
            path = get_download_path()
    try:
        download = audio(url, path)
        if(not download):
            return render_template('error.html')
    except PytubeFixError:
        return render_template('error.html')

    return render_template('hello.html', name = path)

def audio(thelink, path) -> bool:
    try:
        yt = YouTube(thelink, on_progress_callback=on_progress)
        print('Title:', yt.title)
        print('Views:', yt.views)
        video = yt.streams.get_audio_only()
        out_file = video.download(output_path=path, mp3 = True)
        base, ext = os.path.splitext(out_file)
        new_file = Path(f'{base}.mp3')
        os.rename(out_file, new_file)
        if new_file.exists():
            print(f'{yt.title} has been successfully downloaded.')
            return True
        else:
            return False
    except Exception as e:
        print(f'ERROR: {yt.title}could not be downloaded! \n Error: {e}')
        return False

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

if __name__ == "__main__":
    app.run()