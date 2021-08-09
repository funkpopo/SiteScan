import requests

se = requests.session()
url = input()
data = se.get(url)
with open("../download/download.txt", "w+", encoding='UTF-8') as f:
    # utf-8/gbk
    f.write(data.content.decode("utf-8"))
