import requests
from util.common_util import handle_rsp, url_encode
from util.random_util import random_str


def beatiful_content(content: str) -> str:
    # 换行符替换为<p>
    content = "<p>" + content.replace("\n", "<p>")
    return content


def post_article(title: str, content: str) -> str:
    url = "https://mp.toutiao.com/mp/agw/article/publish?source=mp&type=article&aid=1231&_signature=_02B4Z6wo00101Rg9u5wAAIDAxEQkKt8NLnEYOb8AACDjUhdFVyVaijmuW8KJ3dwNFpRMc8lICw7wQ2pCBdMnuOQkHECO5yaE854CfcEIV12D08AlTiQK4-UZRwnl8hauCAi8.EWyMCgR.Aia56"

    # 生成pgc_id样式为7417002138498368059 98368059设置为8位数字
    pgc_id = "74170021384" + random_str(8)
    print(f"pgc_id: {pgc_id}")
    encode_title = url_encode(title)
    encode_content = url_encode(beatiful_content(content))

    payload = f"pgc_id={pgc_id}&source=0&content={encode_content}&title={encode_title}&search_creation_info=%7B%22searchTopOne%22%3A0%2C%22abstract%22%3A%22%22%2C%22clue_id%22%3A%22%22%7D&title_id=1726905375204_1810791264358426&ic_uri_list=&extra=%7B%22content_word_cnt%22%3A902%2C%22is_multi_title%22%3A0%2C%22sub_titles%22%3A%5B%5D%2C%22gd_ext%22%3A%7B%22entrance%22%3A%22%22%2C%22from_page%22%3A%22publisher_mp%22%2C%22enter_from%22%3A%22PC%22%2C%22device_platform%22%3A%22mp%22%2C%22is_message%22%3A0%7D%2C%22tuwen_wtt_trans_flag%22%3A%222%22%2C%22info_source%22%3A%7B%22source_type%22%3A-1%7D%7D&appid_list=&stock_ids=&concern_list=&mp_editor_stat=%7B%22a_left%22%3A1%2C%22color%22%3A1%7D&educluecard=&draft_form_data=%7B%22coverType%22%3A2%7D&pgc_feed_covers=%5B%7B%22id%22%3A%22%22%2C%22url%22%3A%22https%3A%2F%2Fimage-tt-private.toutiao.com%2Ftos-cn-i-6w9my0ksvp%2F46100b679cc74745b62108e8b0d6b154~tplv-tt-cover-v2.image%3F_iz%3D115383%26c%3D811c9dc5%26from%3Dimage_upload%26lk3s%3D72284de7%26policy%3DeyJ2bSI6MywidWlkIjoiNjE2NzYzMTEyNDYifQ%253D%253D%26x-orig-authkey%3D5a21e4afda5945d9a206a695e4c78a63%26x-orig-expires%3D2358057423%26x-orig-sign%3Dq9KhMxcbMutrRx%252BwzpBuLSW6jF0%253D%22%2C%22uri%22%3A%22tos-cn-i-6w9my0ksvp%2F420b4c82c20b41be8735baa8a79b3626%22%2C%22ic_uri%22%3A%22%22%2C%22thumb_width%22%3A719%2C%22thumb_height%22%3A702%2C%22extra%22%3A%7B%22from_content_uri%22%3A%22%22%2C%22from_content%22%3A%220%22%7D%7D%5D&article_ad_type=2&claim_exclusive=1&is_fans_article=0&govern_forward=0&praise=0&disable_praise=0&tree_plan_article=0&star_order_id=&star_order_name=&activity_tag=0&trends_writing_tag=0&is_refute_rumor=0&save=1&timer_status=0&timer_time="
    # payload = f"pgc_id={pgc_id}&source=0&content={encode_content}&title={encode_title}&save=1"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "cookie": "passport_csrf_token=a64517eac455344a6d543e5733b3565b; passport_csrf_token_default=a64517eac455344a6d543e5733b3565b; tt_webid=7416982508770493989; d_ticket=d51a1296ab7db5edce2ca4e15e212a865bd4c; n_mh=ftIS0TwXWQwUlEvUu9YlpySCgR2VroMUlqNkabV2ZZ4; sso_auth_status=ca82fb1c7ee4bd68133df6239a934fdf; sso_auth_status_ss=ca82fb1c7ee4bd68133df6239a934fdf; sso_uid_tt=6ed98e29a92a19ecf17fcca2516a05c9; sso_uid_tt_ss=6ed98e29a92a19ecf17fcca2516a05c9; toutiao_sso_user=7a3cd9bc8bf7083a1ae97bf3d14db5d4; toutiao_sso_user_ss=7a3cd9bc8bf7083a1ae97bf3d14db5d4; sid_ucp_sso_v1=1.0.0-KGRmNGZhNzczMGUzOTA5NzVkOWJhODNiYmE4YjI3YzY0M2ViM2JjYjEKHAjOpcfh5QEQ_9S5twYYGCAMMJz038kFOAJA8QcaAmhsIiA3YTNjZDliYzhiZjcwODNhMWFlOTdiZjNkMTRkYjVkNA; ssid_ucp_sso_v1=1.0.0-KGRmNGZhNzczMGUzOTA5NzVkOWJhODNiYmE4YjI3YzY0M2ViM2JjYjEKHAjOpcfh5QEQ_9S5twYYGCAMMJz038kFOAJA8QcaAmhsIiA3YTNjZDliYzhiZjcwODNhMWFlOTdiZjNkMTRkYjVkNA; passport_auth_status=64f8e2e0ff49f6c1ce7b3db41f1c0475%2Ca7ff19c2b262c1979b46fe033bc91617; passport_auth_status_ss=64f8e2e0ff49f6c1ce7b3db41f1c0475%2Ca7ff19c2b262c1979b46fe033bc91617; sid_guard=1de990c72b9d0cf64a90d0c438ca7f6c%7C1726900863%7C5184001%7CWed%2C+20-Nov-2024+06%3A41%3A04+GMT; uid_tt=8db72d77586e8c863f38f9c5629ae270; uid_tt_ss=8db72d77586e8c863f38f9c5629ae270; sid_tt=1de990c72b9d0cf64a90d0c438ca7f6c; sessionid=1de990c72b9d0cf64a90d0c438ca7f6c; sessionid_ss=1de990c72b9d0cf64a90d0c438ca7f6c; is_staff_user=false; sid_ucp_v1=1.0.0-KDYxMWZkMzRkMzVkZGJkNmE0MTIyYzAwNjg2NGUzZWNjMmQwODBjNmYKFgjOpcfh5QEQ_9S5twYYGCAMOAJA8QcaAmxmIiAxZGU5OTBjNzJiOWQwY2Y2NGE5MGQwYzQzOGNhN2Y2Yw; ssid_ucp_v1=1.0.0-KDYxMWZkMzRkMzVkZGJkNmE0MTIyYzAwNjg2NGUzZWNjMmQwODBjNmYKFgjOpcfh5QEQ_9S5twYYGCAMOAJA8QcaAmxmIiAxZGU5OTBjNzJiOWQwY2Y2NGE5MGQwYzQzOGNhN2Y2Yw; store-region=cn-gd; store-region-src=uid; odin_tt=af0d86575830c1f482437b581f02ed9d25b00eed5245540d39453dee7fce06ffd2c5b76d9e638e210c1371807c1f5734; ttwid=1%7CO50IvIE4ysmbZCG9N3A19bDzqWrFHCE4RKEWQeIICyM%7C1726905115%7C882dca24f6c3d74ecf54ac1ffa4396a35e1bda67d93bf9a95c05886263d11175; gfkadpd=1231,25897; ttcid=c6cf9b62564d4f0bba3b224806397d3019; s_v_web_id=m1buq2km_sNaP1vxL_WlGU_4VX9_9lhq_ALwlDlE56CkE; csrf_session_id=2295ec99ab3a4855cb9a32abc0572b1a; tt_scid=MAfTkIiOPrtGjoUpBD7Zdz-dIJUq6k-nLBe6gjDa5udQpcJkXGB-rcfFqeSXRja0acb9",
        "origin": "https://mp.toutiao.com",
        "priority": "u=1, i",
        "referer": "https://mp.toutiao.com/profile_v4/graphic/publish",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-secsdk-csrf-token": "000100000001e70774a740758a149fd35a27c9605d231efef0afd83379cfc624160be8b7000617f733102271f49d",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return handle_rsp("post_toutiao", response, "text")
