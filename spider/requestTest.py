# 开源的网络请求requests
import requests

r = requests.get("https://www.baidu.com")
print(r.encoding)
print(r.text)
print(r.status_code)
print(r.headers)

print("----------------------------------")
formdata = {
    "i": "生命",
    "from": "AUTO",
    "to": "v",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": "1536850551492",
    "sign": "69caecafb993f3cc30d3b1f11a46228d",
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    "action": "FY_BY_CLICKBUTTION",
    "typoResult": "false"
}

url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "OUTFOX_SEARCH_USER_ID=-552038406@221.234.185.248; OUTFOX_SEARCH_USER_ID_NCOO=344621782.44095385; _ga=GA1.2.245353479.1522311128; P_INFO=17671788208|1534256203|1|youdaonote|00&99|null&null&null#gud&440300#10#0|&0||17671788208; JSESSIONID=aaajMogcd3Xk7cfQAytxw; ___rl__test__cookies=1536850551485",
    "Host": "fanyi.youdao.com",
    "Referer": "http://fanyi.youdao.com/"
}

response = requests.post(url, data=formdata, json=headers)

print(response.text)

# 如果是json文件可以直接显示
print(response.json())