import json

import requests
from common.logger import log
from util.common_util import handle_rsp

url = "http://159.75.168.215/v1/workflows/run"


payload = json.dumps(
    {
        "inputs": {"link": "https://rsshub.app/eastmoney/search/web3"},
        "files": [],
        "response_mode": "streaming",
        "user": "airflow",
    }
)


def run_workflow(api_token: str):
    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, timeout=5 * 60
    )

    content = handle_rsp("run_workflow", response, "text")
    # 获取最后一个处理结果
    content = content.strip()
    json_data = content.split("data: ")[-5]
    result = json.loads(json_data)
    log.info("workflow handle result: %s", result)
    return result


if __name__ == "__main__":
    API_KEY = "app-WhaGmFH3fVZKwppabn09ea4G"
    API_KEY2 = "app-SwSFypeqjzNMQ0Nj65z2n18H"
    run_workflow(API_KEY2)
