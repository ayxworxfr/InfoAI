from jingritoutiao import post_article
from run_task import run_workflow
from util.random_util import random_str


def _test_run_workflow():
    API_KEY = "app-SwSFypeqjzNMQ0Nj65z2n18H"
    result = run_workflow(API_KEY)
    title = result["data"]["title"]
    content = result["data"]["outputs"]["text"]
    print("title:", title)
    print("content:", content)


# 30 7 * * * root /bin/bash /data/home/graycen/project/dags/daily_post.sh
# /data/home/graycen/project/dags/daily_post.sh
def _test_post_article():
    # post_jingritoutiao()
    content = "每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要每日实事摘要"
    post_article("每日实事摘要", content)


def test_rand_str():
    result = random_str(5)
    assert len(result) == 5
