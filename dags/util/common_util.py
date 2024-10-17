import urllib

from common.logger import log


def url_decode(url: str) -> str:
    return urllib.parse.unquote(url)


def url_encode(content: str) -> str:
    result = urllib.parse.quote(content)
    return result


def handle_rsp(action: str, rsp: str, style: str = "json") -> dict:
    if rsp.status_code / 100 != 2:
        log.error(
            "action: %s, status code: %s, response: %s",
            action,
            rsp.status_code,
            rsp.text,
        )
        return None
    log.debug(
        "action: %s, status code: %s, response: %s", action, rsp.status_code, rsp.text
    )
    if style == "json":
        return rsp.json()
    else:
        return rsp.text
