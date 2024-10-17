# -*- coding: utf-8 -*-

from common.logger import log
from jingritoutiao import post_article
from run_task import run_workflow
from toutiao import post_toutiao
from weixin.article import ArticleImpl


def get_article():
    API_KEY = "app-SwSFypeqjzNMQ0Nj65z2n18H"
    result = run_workflow(API_KEY)
    title = result["data"]["title"]
    content = result["data"]["outputs"]["text"]

    log.info("title: %s, content: %s", title, content)
    return content


def post_jingritoutiao():
    content = get_article()
    # post_article("每日实事摘要", content)
    post_toutiao("每日实事摘要", content)
    log.info("post article success")


def post_weixin():
    content = get_article()
    if '"data"' in content:
        log.error("get article failed, err: %s", content)
        return

    result = ArticleImpl().post("每日实事摘要", content)
    if not result:
        log.error("post article failed")
        return
    log.info("post article success")


if __name__ == "__main__":
    # post_jingritoutiao()
    post_weixin()
