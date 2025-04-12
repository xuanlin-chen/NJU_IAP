from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()

    # 设置多个 Cookie
    cookies = [
        {
            "name": "CASTGC",
            "value": "TGT-102973-wSjMoeUMa6Ihe1cGUt7WwHcHwesUgpoIqT6N4Oo4vRLW9rvx4F1744255470740-4hS6-cas",
            "domain": ".nju.edu.cn",
            "path": "/",
            "expires": -1,
            "httpOnly": True,
            "secure": True
        }
        
    ]

    context.add_cookies(cookies)

    page = context.new_page()
    response = context.request.get("https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fndwy.nju.edu.cn%2Fdztml%2F")    
    #print(response.headers().decode('utf-8',errors='ignore'))
    #print(response.body().decode('utf-8', errors='ignore'))
    page.goto("https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fndwy.nju.edu.cn%2Fdztml%2F")
    page.wait_for_load_state("networkidle")
    #nxt = page.get_by_text("嵇煜人").click()
    #aa = page.locator("css=div[class=hd-mc]")
    #for i in range(aa.count()):
    #    a = aa.nth(i)
    #    print(a.text_content())
    
