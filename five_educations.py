from curl_cffi import requests

cookie = {"CASTGC":"TGT-67459-tyIaC3N2073OAC4xMfYhcvnL1NOz5UVVJgvjym1XHur0XEOnH41744109918383-ppeI-cas",
          "route":"32611566dbcd3ae93924d90896c67309",
          "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE":"zh_CN",
          "JSESSIONID_auth":"HAgVDSiNh7N69sEi9GSOH8KMsi8RDLr9mCEbRMUS3vRjEpEoQNeX!-1512314384"}

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133a.0.0.0 Safari/537.36"
headers = {
    "User-Agent": user_agent
}

r = requests.get("https://ndwy.nju.edu.cn/dztml/#/https://authserver.nju.edu.cn/authserver/login?service=https%3A%2F%2Fndwy.nju.edu.cn%2Fdztml%2F", headers=headers
                ,impersonate="chrome133a", cookies=cookie,allow_redirects=False)

if r.status_code == 302:
    print(r.headers)
print(r.status_code)
