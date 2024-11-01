import requests
from bs4 import BeautifulSoup

# 账号信息
username = "15077306061"
password = "zj242655"
# 发布内容
post_content = "这里是你要发布的内容"
# 登录小红书账号
login_url = "https://www.xiaohongshu.com/user/login"
login_data = {
    "username": username,
    "password": password,
}
print("fetch cookie start")
response = requests.post(login_url, data=login_data)
soup = BeautifulSoup(response.text, "html.parser")
print(
    f"fetch cookie success, status: {response.status_code}, cookies: {response.cookies}"
)
cookies = response.cookies
# 获取发布内容的URL和数据
post_url = "https://www.xiaohongshu.com/post/new"
headers = {
    "Referer": "https://www.xiaohongshu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
}
post_data = {
    "title": "标题",  # 填写发布的标题
    "content": post_content,  # 填写要发布的内容
    # 其他可选参数...
}
response = requests.post(post_url, headers=headers, cookies=cookies, data=post_data)
soup = BeautifulSoup(response.text, "html.parser")
if response.status_code == 200:
    print("发布成功！")
else:
    print("发布失败！")
