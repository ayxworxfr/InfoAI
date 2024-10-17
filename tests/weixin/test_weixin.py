from common.logger import log
from toutiao import CONTENT
from weixin.article import Article, ArticleImpl
from weixin.fetch_token import fetch_token

THUMB_MEDIA_ID = "HhX3c8PuBqdnZP8vxxgig-ecC3zXvj0fz5_u0uli0nkfbfOYQOD-xHqaqf8bV9oa"
DRAFT_MEDIA_ID = "HhX3c8PuBqdnZP8vxxgig4cvhHNmm8Mg1Pepc4hfAZWh5PUdUkdCClgDfbGdw-N4"
token = fetch_token()


def _test_fetch_token():
    token = fetch_token()
    assert token is not None


def _test_create_draft():
    article = Article(
        title="今日热点",
        content=Article.beautify_content(CONTENT),
        digest=Article.get_digest(CONTENT),
        thumb_media_id=THUMB_MEDIA_ID,
    )
    impl = ArticleImpl(token)
    media_id = impl.create_draft(article)
    log.info("create draft media_id: %s", media_id)


def test_post_article():
    impl = ArticleImpl(token)
    data = impl.post_draft(DRAFT_MEDIA_ID)
    log.info("post draft: %s", data)


def _test_upload_meterial():
    impl = ArticleImpl(token)
    data = impl.upload_meterial("tests/resources/image01.jpg")
    log.info("media_id: %s, url: %s", data["media_id"], data["url"])
