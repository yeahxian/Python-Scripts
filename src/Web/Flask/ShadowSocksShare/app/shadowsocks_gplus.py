#!/usr/bin/env python
import requests
import re
url = 'http://www.ssglobal.me/wp/blog/2017/02/22/%E8%B4%A6%E5%8F%B7%E5%88%86%E4%BA%AB/'
url2 = 'https://plus.google.com/communities/103542666306656189846/stream/dd570c04-df51-4394-8c83-eabb12cc0d0c'

def main():
    data = list()
    try:
        data += re.findall('ssr?://\w+', requests.get(url, verify=False).text)
    except Exception:
        pass
    try:
        data += re.findall('ssr?://\w+', requests.get(url2, verify=False).text)
    except Exception:
        pass
    return data


if __name__ == '__main__':
    data = main()
    for i in data:
        print(i)
