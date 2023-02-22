import urllib.request

import chardet
from bs4 import BeautifulSoup


def web_scrap_return_text(url):

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('p')
    encoding = soup.original_encoding or 'utf-8'

    text = ""

    for i in range(0, len(data)):
        if("সম্পাদক" in data[i].text) or ("সূত্র:" in data[i].text):
            break
        data[i].text.encode(encoding)
        text = text+data[i].text

    return text

