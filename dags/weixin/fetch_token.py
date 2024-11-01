import requests
from common.logger import log
from util.common_util import handle_rsp

APP_ID = "wx9e3d9721cc84880a"
APP_SECRET = "886b9eab8c0c7a5fc294de9889c5c2d1"


def fetch_token():
    URL = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    rsp = requests.get(URL)
    data = handle_rsp("fetch_token", rsp)
    return data["access_token"]
