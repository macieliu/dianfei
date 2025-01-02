import os
import requests
from bs4 import BeautifulSoup

APPTOKEN = os.environ.get("APPTOKEN")
UIDS = os.environ.get("UIDS")
SYSID = os.environ.get("SYSID")
ROOMID = os.environ.get("ROOMID")
AREAID = os.environ.get("AREAID")
BUILDID = os.environ.get("BUILDID")
TOPICIDS = os.environ.get("TOPICIDS")


def fetch_electricity_bill_html(sysid, roomid, areaid, buildid):
    url = f"https://epay.sues.edu.cn/epay/wxpage/wanxiao/eleresult?sysid={sysid}&roomid={roomid}&areaid={areaid}&buildid={buildid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.8.9 Wmxy/5.8.10"
    }

    try:
        # 发送 GET 请求，设置超时时间为 10 秒
        response = requests.get(url=url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return None


def extract_left_degree(html):
    soup = BeautifulSoup(html, "html.parser")
    input_tag = soup.find("input", {"left-degree": True})
    left_degree_value = float(input_tag["left-degree"])
    return left_degree_value


def wxpusher(content):
    headers = {"content-type": "application/json"}
    webapi = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": APPTOKEN,
        "content": content,  # 主体内容
        "contentType": 1,  # 文本
        "topicIds": [TOPICIDS],  # 主题id
    }
    result = requests.post(url=webapi, json=data, headers=headers)
    return result.text


def monitor_power():
    html_content = fetch_electricity_bill_html(
        sysid=SYSID, roomid=ROOMID, areaid=AREAID, buildid=BUILDID
    )

    if html_content:
        electricity_degree = extract_left_degree(html_content)
        print(f"剩余电费：{electricity_degree}")
        if electricity_degree < 20:
            result = wxpusher(f"剩余电费：{electricity_degree}，电量即将耗尽请立即充值")
            print(result)
            print("电量即将耗尽请立即充值")
        else:
            result = wxpusher(f"剩余电费：{electricity_degree}，电量充足无需充值")
            print(result)
            print("电量充足无需充值")


monitor_power()
