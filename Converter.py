from pytubefix import YouTube
import os
from pathlib import Path


def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in " ._-" else "_" for c in filename)


def audio(thelink, path):
    try:
        yt = YouTube(thelink)
        print('Title:', yt.title)
        print('Views:', yt.views)
        video = yt.streams.filter(abr='160kbps').last()
        out_file = video.download(output_path=path)
        base, ext = os.path.splitext(out_file)
        new_file = Path(f'{base}.mp3')
        os.rename(out_file, new_file)
        if new_file.exists():
            print(f'{yt.title} has been successfully downloaded.')
    except Exception as e:
        print(f'ERROR: {yt.title}could not be downloaded! \n Error: {e}')

def high(thelink, path):
    print('Attempting to download high quality video and audio')
    try:
        yt = YouTube(thelink)
        print('Title:', yt.title)
        print('Views:', yt.views)
        yt_title = sanitize_filename(yt.title)

        # Download the highest resolution video with a specified filename
        video_stream = yt.streams.filter().order_by("resolution").last()
        audio_stream = yt.streams.get_audio_only()

        video_filename = f'{yt_title}.mp4'
        audio_filename = f'{yt_title}.mp3'

        video_stream.download(output_path=path, filename=video_filename)
        audio_stream.download(output_path=path, filename=audio_filename)

        print('Finished downloading high resolution video and audio')

    except Exception as e:
        print(f'ERROR: {yt.title}could not be downloaded! \n Error: {e}')


def low(thelink, path):
    print('Attempting to download low resolution video')
    try:
        yt = YouTube(thelink)
        print('Title:', yt.title)
        print('Views:', yt.views)
        yd = yt.streams.get_lowest_resolution()
        yt_title = sanitize_filename(yt.title)
        yd.download(output_path=path, filename=f'{yt_title}.mp4')
        print('Finished downloading low resolution video')
    except Exception as e:
        print(f'ERROR: {yt.title}could not be downloaded! \n Error: {e}')


link_inp = input("Please Enter the link of the video: ")
path_inp = input("Please Enter the download path: ")
menu_inp = input('Select:\n1- Audio\n2- Highest Resolution\n3- Lowest Resolution\n')

if menu_inp == '1':
    audio(link_inp, path_inp)
elif menu_inp == '2':
    high(link_inp, path_inp)
elif menu_inp == '3':
    low(link_inp, path_inp)
else:
    print('Invalid input')