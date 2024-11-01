import json
from dataclasses import dataclass
from typing import Iterable, Union

import requests
from common.logger import log
from util.constraints import CHARS
from weixin.fetch_token import fetch_token, handle_rsp

BASE_DOMAIN = "https://api.weixin.qq.com"
THUMB_MEDIA_ID = "HhX3c8PuBqdnZP8vxxgig-ecC3zXvj0fz5_u0uli0nkfbfOYQOD-xHqaqf8bV9oa"


@dataclass
class Article:
    title: str = ""
    content: str = ""
    thumb_media_id: str = THUMB_MEDIA_ID  # 封面图片
    author: str = "InfoAI517"
    digest: str = ""  # 摘要
    show_cover_pic: int = 1
    content_source_url: str = ""
    need_open_comment: int = 0
    only_fans_can_comment: int = 0

    @classmethod
    def get_digest(cls, content: str) -> str:
        # 如果是符号就取前一个字符直到不是符号
        idx = 30
        while content[idx] in CHARS:
            idx -= 1
        return content[:idx]

    @classmethod
    def beautify_content(cls, content: str) -> str:
#        return content.replace("\n", "<br/>")
        # 拆分文本到列表，分隔符为一个或多个换行符
        parts = content.split('\n')
        
        # 过滤掉空字符串，这可能由连续的换行符产生
        parts = [part for part in parts if part.strip()]
        
        # 将每个非空部分用标签包裹
        br = '<br style="style="-webkit-tap-highlight-color: transparent; outline: 0px; font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; letter-spacing: 0.544px; text-wrap: wrap; background-color: rgb(255, 255, 255); visibility: visible;">'
        html_parts = [f'<span style="font-family: &quot;PingFang SC&quot;, system-ui, -apple-system, BlinkMacSystemFont, &quot;Helvetica Neue&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei UI&quot;, &quot;Microsoft YaHei&quot;, Arial, sans-serif; letter-spacing: 0.544px; text-wrap: wrap; background-color: rgb(255, 255, 255); visibility: visible;">{part}</span>{br}{br}' for part in parts]
        
        # 将所有部分合并为一个字符串
        html_text = ''.join(html_parts)
        
        return f'<p style="visibility: visible; margin-bottom: 0px;">{html_text}</p>'


class ArticleImpl:
    def __init__(self, access_token: str = None):
        self.access_token = access_token

    def post(self, title: str, content: str) -> dict:
        if self.access_token is None:
            self.access_token = fetch_token()

        article = Article(
            title=title,
            content=Article.beautify_content(content),
            digest=Article.get_digest(content),
        )
        media_id = self.create_draft(article)
        #return None
        if not media_id:
            return None
        return self.post_draft(media_id)

    def create_draft(self, articles: Union[Article, Iterable[Article]]) -> str:
        POST_DRAFT_URL = (
            f"{BASE_DOMAIN}/cgi-bin/draft/add?access_token={self.access_token}"
        )
        if isinstance(articles, Article):
            articles = [articles]
        dict_data = {"articles": [article.__dict__ for article in articles]}
        rsp = requests.post(POST_DRAFT_URL, data=self.trans2json(dict_data))
        data = handle_rsp("post_draft", rsp)
        if data.get("media_id"):
            return data.get("media_id")
        log.error("create draft failed, err: %s", data.get("errmsg"))
        return None

    def post_draft(self, media_id: str) -> dict:
        POST_DRAFT_URL = (
            f"{BASE_DOMAIN}/cgi-bin/freepublish/submit?access_token={self.access_token}"
        )
        rsp = requests.post(
            POST_DRAFT_URL, data=self.trans2json({"media_id": media_id})
        )
        data = handle_rsp("post_draft", rsp)
        if data.get("errcode") == 0:
            return data
        log.error("post draft failed, err: %s", data.get("errmsg"))
        return data

    def upload_meterial(self, file_path: str, type: str = "image") -> dict:
        UPLOAD_MEDIA_URL = f"{BASE_DOMAIN}/cgi-bin/material/add_material?type={type}&access_token={self.access_token}"
        files = [("media", open(file_path, "rb"))]
        rsp = requests.post(UPLOAD_MEDIA_URL, files=files)
        data = handle_rsp("upload_material", rsp)
        return data

    def trans2json(self, data: dict) -> str:
        return json.dumps(data, ensure_ascii=False).encode("utf-8")
