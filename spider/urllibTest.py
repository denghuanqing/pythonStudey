# urllib2在python3.*中改为urllib.request  演示urllib.request用法
import urllib.request
import urllib.parse

response = urllib.request.urlopen("https://www.lagou.com/zhaopin/Java/")
print(response.read())
print("---------------------------")

url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
formdata = {
    "type":"AUTO",
    "i":"i love python",
    "doctype":"json",
    "xmlVersion":"1.8",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_ENTER",
    "typoResult":"true"
}
data = urllib.parse.urlencode(formdata).encode("UTF-8")

ua_header = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
request = urllib.request.Request(url, data=data, headers=ua_header)
response2 = urllib.request.urlopen(request)
print (response2.read())
print("---------------------------")
