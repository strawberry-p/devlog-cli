import requests as r
from bs4 import BeautifulSoup
PROJECT_ID = "12788"
PROJECT_PREFIX = "https://summer.hackclub.com/projects/"
page_html = r.get(f"{PROJECT_PREFIX}{PROJECT_ID}")
print(page_html.text)
soup = BeautifulSoup(page_html.text,"html.parser")
formParent = soup.find_all("form",attrs={"data-controller": "form devlog-attachment-paste"})
print(formParent)