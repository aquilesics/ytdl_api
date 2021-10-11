from flask import Flask
from flask import request


app = Flask(__name__)
app.config["CLIENT_SONGS"] = "/home/junior/repos/github.com/aquilesics/ytdl_api/app/_tmp/"

from app import view