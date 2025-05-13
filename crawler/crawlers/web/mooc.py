from curl_cffi import requests

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
refer = "https://www.icourse163.org/passport/logingate/changeCookie.htm?type=study&returnUrl=aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvaG9tZS5odG0_dXNlcklkPTE1NzU3MzIzMjA&loginWay=0"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Accept": accept,
    "Cache-Control": "max-age=0",
    "Referrer": refer,
}
r = requests.post(
    "https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc?csrfKey=823e78895bf441c4a122df0e40a5b58f",
    headers=headers,
    impersonate="chrome"
)
print(r.status_code)
print(r.text)
