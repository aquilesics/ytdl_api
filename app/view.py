from os import abort, error, path
import os
from flask import Response
from flask.json import dump
from app import app
import youtube_dl
from utils import ydl_opts
from flask import request, jsonify
from flask import send_file, send_from_directory
from flask import stream_with_context
import time


filtro = [
    'categories', 'channel', 'chapters', 'display_id', 'duration', 'extractor', 'webpage_url', 'webpage_url_basename', 'view_count', 'categories',
     'channel', 'chapters', 'display_id', 'duration', 'extractor', 'webpage_url', 'webpage_url_basename', 'view_count', 'title', '_type', 'thumbnail', 'entries'
]


def clear_info(raw_info) -> dict:
    clean_info = dict(filter(lambda x: x[0] in filtro, raw_info.items()))
    if "_type" in clean_info:
        clean_info["entries"] = list(
            map(lambda x: clear_info(x), clean_info["entries"]))

    return dict(clean_info)


@app.route('/')
def index():
    return "Hello from Flask"

# ZnqskQOzYxc jon b
# k1k6EUW0czc sade


@app.route('/info/', methods=['GET'])
def get_info():
    req = request.get_json()
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(req['url'], download=False)

        return clear_info(info)
    except:
        return 'bad request!', 400


def process(_req):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(_req['url'], download=True)
        print("" + info['title'] + ".mp3")

    return info
           

@app.route('/download')
def get_download(): 
    req = request.get_json()
    info = process(req)
    print("download in -->", os.getcwd())
        
    return send_from_directory(r"./app/_tmp/", path=f'{info["title"]}.mp3', as_attachment=True)
  
    
# @app.after_request
# def delete_files(Response):
#     p = os.getcwd() + "/app/tmp/"
#     for file in os.listdir(p):
#         os.remove(f"{p}/{file}")
#     return Response