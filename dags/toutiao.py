from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL = 'https://mp.toutiao.com/profile_v4/index'
SLEEP_TIME = 2
COOKIE = 'gfkadpd=1231,25897; csrf_session_id=ddd0e8ddbd1eb1434c8d251c74ae0b30; passport_csrf_token=d05c9b1da6c0af027a46e7e96f7bc0ab; passport_csrf_token_default=d05c9b1da6c0af027a46e7e96f7bc0ab; s_v_web_id=verify_m1gcc8od_BhaNyHUk_UUj8_4HEW_BGRC_Rsctlg6B7dO0; ttwid=1%7CHnxflnBYZpGZezA9rETIOl8yynsZZrtbFER2R7BDrtY%7C1727176577%7C255c688cfdb28b9ed500da8965073600eb0f4df71798cf6c72c6f19636b41289; n_mh=ftIS0TwXWQwUlEvUu9YlpySCgR2VroMUlqNkabV2ZZ4; sso_uid_tt=09c53507e0c6352d90bfc922aa0c6811; sso_uid_tt_ss=09c53507e0c6352d90bfc922aa0c6811; toutiao_sso_user=3457d89db47ca30afe4691bc121341eb; toutiao_sso_user_ss=3457d89db47ca30afe4691bc121341eb; sid_ucp_sso_v1=1.0.0-KGI4NGExOTI5ODhhMmYwN2MyY2FhMzU3ZGVmMDNiZWZkNmZmNjU3NzYKHQjOpcfh5QEQib_KtwYYzwkgDDCc9N_JBTgGQPQHGgJobCIgMzQ1N2Q4OWRiNDdjYTMwYWZlNDY5MWJjMTIxMzQxZWI; ssid_ucp_sso_v1=1.0.0-KGI4NGExOTI5ODhhMmYwN2MyY2FhMzU3ZGVmMDNiZWZkNmZmNjU3NzYKHQjOpcfh5QEQib_KtwYYzwkgDDCc9N_JBTgGQPQHGgJobCIgMzQ1N2Q4OWRiNDdjYTMwYWZlNDY5MWJjMTIxMzQxZWI; passport_auth_status=ad01616d46fad8e77eb768087a877229%2C; passport_auth_status_ss=ad01616d46fad8e77eb768087a877229%2C; sid_guard=f3b29c93814dd0046e3da160df0a336a%7C1727176586%7C5184001%7CSat%2C+23-Nov-2024+11%3A16%3A27+GMT; uid_tt=12907a5deccdaf36a80f7333e7157f93; uid_tt_ss=12907a5deccdaf36a80f7333e7157f93; sid_tt=f3b29c93814dd0046e3da160df0a336a; sessionid=f3b29c93814dd0046e3da160df0a336a; sessionid_ss=f3b29c93814dd0046e3da160df0a336a; is_staff_user=false; sid_ucp_v1=1.0.0-KDRjZWRkODA5YWFlOGIxMjEzYTdiOTA3YmNiMzQ1N2ViOTQxMzA1ZjQKFwjOpcfh5QEQir_KtwYYzwkgDDgGQPQHGgJsZiIgZjNiMjljOTM4MTRkZDAwNDZlM2RhMTYwZGYwYTMzNmE; ssid_ucp_v1=1.0.0-KDRjZWRkODA5YWFlOGIxMjEzYTdiOTA3YmNiMzQ1N2ViOTQxMzA1ZjQKFwjOpcfh5QEQir_KtwYYzwkgDDgGQPQHGgJsZiIgZjNiMjljOTM4MTRkZDAwNDZlM2RhMTYwZGYwYTMzNmE; store-region=cn-gd; store-region-src=uid; odin_tt=f1f3ffe7ffdb9e1836850333728e90ac9f63af33ba17eb2e1aad207ba3113d558e1bcc44f70715092ac61f96fbc89c94; ttcid=97c90b962afd498f944882930c91616e21; tt_scid=OA46RFpafvqWl0etsOnlhjRNGx..cKRBnX.7hpKcqkTd0rW91PYcE02HKJxLbpTkd3cf'

def parse_cookies(cookie:str, domain:str)->dict[str, str]:
    cookie_list = []
    for cookie in cookie.split('; '):
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookie_dict = {
                'name': key.strip(),
                'value': value.strip(),
                'path': '/',
                'domain': domain
            }
            cookie_list.append(cookie_dict)
    return cookie_list

def set_cookies(driver, cookies: str):
    driver.get(URL) # 必须先打开网页
    cookies = parse_cookies(cookies, URL.split('/')[2])
    for cookie in cookies:
        if 'name' in cookie and 'value' in cookie:
            driver.add_cookie(cookie)

def set_window_size(driver, width = 1920, height = 1080):
    # # 最大化窗口
    # driver.maximize_window()
    driver.set_window_size(width, height)

def scroll(driver, y:int=0, xpath:str = None):
    if xpath:
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView();", element)
    else:
        js = f"window.scrollTo(0, {y});"
        driver.execute_script(js)

def login(driver):
    account = "15332780894"
    pwd = "xsy19980905"
    p_login_click_xpath = '//*[@id="BD_Login_Form"]/div/article/article/div[2]/div/ul/li[4]'
    ty_click_xpath = '//*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[4]/span[1]'
    ph_input_xpath = '//*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[1]/div/input'
    p_input_xpath = '//*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[2]/div/div/input'
    dl_click_xpath = '//*[@id="BD_Login_Form"]/div/article/article/div[1]/div[1]/div[2]/article/div[5]/button'

    driver.get(URL) # 打开网页
    time.sleep(SLEEP_TIME)

    write_click = driver.find_element(By.XPATH, p_login_click_xpath)
    write_click.click()
    time.sleep(SLEEP_TIME)

    ty_click = driver.find_element(By.XPATH, ty_click_xpath)
    ty_click.click()
    time.sleep(SLEEP_TIME)

    ph_input = driver.find_element(By.XPATH, ph_input_xpath)
    ph_input.send_keys(account)
    time.sleep(SLEEP_TIME)

    p_input = driver.find_element(By.XPATH, p_input_xpath)
    p_input.send_keys(pwd)
    time.sleep(SLEEP_TIME)

    dl_click = driver.find_element(By.XPATH, dl_click_xpath)
    dl_click.click()
    time.sleep(SLEEP_TIME)

def post_data(driver, title: str, content: str):
    # 定义 XPath 变量
    write_click_xpath = '//*[@id="masterRoot"]/div/div[3]/section/aside/div/div/div/div[2]/div[2]/div[1]/span/a'
    title_input_xpath = '//*[@id="root"]/div/div[1]/div/div[1]/div[3]/div/div/div[2]/div/div/div/textarea'
    content_input_xpath = '//*[@id="root"]/div/div[1]/div/div[1]/div[4]/div/div[1]'
    image_click_xpath = '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div'
    my_image_click_xpath = '/html/body/div[20]/div[2]/div/div/div[2]/div/div[1]/div/div/div/div[3]'
    choice_image_click_xpath = '/html/body/div[20]/div[2]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/span[2]'
    first_click_xpath = '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[4]/div[2]/div/div[1]/label/span/div'
    sure_click_xpath = '/html/body/div[20]/div[2]/div/div/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/button[2]'
    publish_click_xpath = '//*[@id="root"]/div/div[1]/div/div[3]/div/button[3]'
    check_click_xpath = '//*[@id="root"]/div/div[1]/div/div[3]/div/button[2]'

    # 点击写文章按钮
    write_click = driver.find_element(By.XPATH, write_click_xpath)
    write_click.click()
    time.sleep(SLEEP_TIME)

    # 输入标题
    title_input = driver.find_element(By.XPATH, title_input_xpath)
    title_input.send_keys(title)
    time.sleep(SLEEP_TIME)

    # 输入内容
    content_input = driver.find_element(By.XPATH, content_input_xpath)
    content_input.send_keys(content)
    time.sleep(SLEEP_TIME)

    scroll(driver, xpath='//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div[1]/span')
    time.sleep(SLEEP_TIME)
    # 点击添加图片
    image_click = driver.find_element(By.XPATH, image_click_xpath)
    image_click.click()
    time.sleep(SLEEP_TIME)

    # 选择我的图片
    my_image_click = driver.find_element(By.XPATH, my_image_click_xpath)
    my_image_click.click()
    time.sleep(SLEEP_TIME)

    # 选中具体的图片
    choice_image_click = driver.find_element(By.XPATH, choice_image_click_xpath)
    choice_image_click.click()
    time.sleep(SLEEP_TIME)

    # 点击确定按钮
    sure_click = driver.find_element(By.XPATH, sure_click_xpath)
    sure_click.click()
    time.sleep(SLEEP_TIME)

    # 取消首发
#    first_click = driver.find_element(By.XPATH, first_click_xpath)
#    first_click.click()
#    time.sleep(SLEEP_TIME)

    # 发布文章
    publish_click = driver.find_element(By.XPATH, publish_click_xpath)
    publish_click.click()
    time.sleep(3*SLEEP_TIME)

    # 确认发布
    check_click = driver.find_element(By.XPATH, check_click_xpath)
    check_click.click()
    time.sleep(3*SLEEP_TIME)


    # 结束操作，关闭浏览器
    driver.quit()

CONTENT = """在浩瀚的数字宇宙中，Web3的概念如同一颗冉冉升起的新星，引领着我们步入了第三代互联网的新时代。它不仅仅是技术的革新，更是思维方式的转变，预示着一个安全透明、用户拥有更多控制权的网络生态。在这个新纪元里，我们见证了算力设备品牌的崛起，加密货币项目的亮相，以及区块链技术的蓬勃发展。

港交所今年新上市的ETF产品数目达28只，其中不乏投资于人工智能、数码支付、Web3等前沿领域的新ETF。这些主题式ETF近年增长可观，今年首八个月的平均每日成交额已超过21亿港元，资产管理规模于8月底达到631亿港元，展现了亚洲增长的潜力。

聪链集团的上海小众芯片公司Goldshell，凭借其在WEB3行业的认可度，成功突围。WEB3，这个泛指第三代互联网应用的发展概念，正逐渐成为算力设备和其他WEB3基础设施相关硬件和软件产品的新战场。

在重庆，一场文化的盛宴——第十三届重庆文博会，通过先进的Web3D技术，将3D虚拟展厅和摄影师共创产品呈现在了公众面前，让我们得以在云端欣赏多彩的巴渝文化。

特朗普家族支持的加密货币项目，更是将“名人效应”带入了币圈。特朗普本人被称为“首席加密货币倡导者”，其家族成员也纷纷担任了项目的“DeFi远见者”和“Web3大使”，这无疑为Web3领域增添了不少话题。

在学术界，肖钢、朱嘉明等专家在外滩大会上共议资产通证化引领Web3向实。他们认为，尽管Web3产业整体发展仍处于早期阶段，但Web3和AI大模型的结合有助于其核心价值的实现。

蚂蚁数科CEO赵闻飙在外滩大会上表示，过去一年客户数增长35%，将发力产业Web3与技术出海战略。蚂蚁数科长期投入Web3技术创新研发，打造了高性能、大规模的区块链网络架构HOU，并支持跨链互联。

肖钢认为，Web3可以为做好金融“五篇大文章”提供有力支撑，它不仅仅是技术的革新，更是思维方式的转变，预示着安全透明、用户拥有更多控制权的网络生态。

8月份全球Web3领域融资8.18亿美元，虽然环比下降14.08%，但Web3融资总额依然可观，显示出全球投资者对Web3领域的信心。

互联网大厂纷纷入局稳定币，全球支付江湖百年变局来临。香港Web3能否成为制胜的“跳板”？阿里现任掌舵人蔡崇信是Web3的坚定支持者，家族的蓝池资本投资了早期的FTX、polygon、Animoca等知名Web3项目。

在这个科技迅猛发展的时代，Web3正以其独特的魅力，吸引着全球的目光。它不仅仅是技术的迭代，更是一场关于价值互联的革命。让我们拭目以待，Web3将如何塑造我们的未来。
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# 绕过检测
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)


service = Service(ChromeDriverManager().install())

def post_toutiao(title, content):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # set_cookies(driver, COOKIE)
    login(driver)
    driver.get(URL)
    set_window_size(driver)

    post_data(driver, title, content)

if __name__ == '__main__':
    post_toutiao("文章标题", CONTENT)
    # driver = webdriver.Edge()  # 指定 WebDriver 的路径
    # driver.get('https://www.baidu.com')  # 打开网页
    # time.sleep(2)  # 等待两秒


