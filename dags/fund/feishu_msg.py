import base64
import hashlib
import hmac
import json
import time

import requests
from common.logger import log


class FeishuBot:
    def __init__(self, webhook_url, secret):
        self.webhook_url = webhook_url
        self.secret = secret

    def _generate_signature(self, timestamp):
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"), msg=b"", digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(hmac_code).decode("utf-8")

    def _send_message(self, payload):
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.webhook_url, headers=headers, data=json.dumps(payload)
        )
        return response

    def send_text_message(self, text, title=None):
        timestamp = str(int(time.time()))
        sign = self._generate_signature(timestamp)

        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "text",
            "content": {"text": text},
        }
        response = self._send_message(payload)
        return response.text

    def send_table_message(self, columns, rows, title=None, page_size=10):
        timestamp = str(int(time.time()))
        sign = self._generate_signature(timestamp)

        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {
                    "template": "blue",
                    "title": {
                        "content": title if title else "Table",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "table",
                        "page_size": page_size,
                        "row_height": "low",
                        "header_style": {
                            "text_align": "center",
                            "text_size": "normal",
                            "background_style": "none",
                            "text_color": "default",
                            "bold": True,
                            "lines": 1,
                        },
                        "columns": columns,
                        "rows": rows,
                    },
                ],
            },
        }
        response = self._send_message(payload)
        return response.text


def send_feishu_msg(text=None, columns=None, rows=None, title=None):
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/22c4229d-5db7-4c2b-b089-f3fea20c07d3"
    secret = "wcAcSdyIxYepciPRzFouDc"
    bot = FeishuBot(webhook_url, secret)

    rsp = None
    if text:
        rsp = bot.send_text_message(text, title)
    elif columns and rows:
        rsp = bot.send_table_message(columns, rows, title)
    log.info("Feishu message sent end: %s", rsp)
    return rsp


if __name__ == "__main__":
    # Define simplified table configuration
    columns = [
        {"name": "customer_name", "display_name": "客户名称", "data_type": "text"},
        {"name": "customer_link", "display_name": "相关链接", "data_type": "lark_md"},
        {"name": "customer_arr", "display_name": "ARR(万元)", "data_type": "number"},
    ]
    rows = [
        {
            "customer_name": "飞书科技",
            "customer_link": "[飞书科技](/ssl:ttdoc/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message-reaction/emojis-introduce)",
            "customer_arr": 168.23,
        },
        {
            "customer_name": "飞书科技_01",
            "customer_link": "[飞书科技_01](/ssl:ttdoc/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message-reaction/emojis-introduce)",
            "customer_arr": 123.45,
        },
    ]
    response = send_feishu_msg(columns=columns, rows=rows, title="Custom Table Title")
