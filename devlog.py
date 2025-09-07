import requests as r
from bs4 import BeautifulSoup
import json
import sys, os
PROJECT_ID = "12788"
PROJECT_PREFIX = "https://summer.hackclub.com/projects/"
with open("session.json") as session_file:
    session_cookies = json.load(session_file)
cookie = ""
for key,value in session_cookies.items():
    cookie += f"{key}={value};"
cookie = cookie[:-1]
s = r.Session()
s.headers.update({"Cookie":cookie})
page_html = s.get(f"{PROJECT_PREFIX}{PROJECT_ID}")
soup = BeautifulSoup(page_html.text,"html.parser")
formParent = soup.find_all("form",attrs={"data-controller": "form devlog-attachment-paste"})[0]
print(f"\n ======= \n")
authenticity = formParent.find("input",attrs={"name":"authenticity_token"})["value"]
print(authenticity)
s_devlog = r.Session()
s_devlog.headers.update({"Cookie": cookie}) #can't add the authenticity csrf token, it might change
FORM_BOUNDARY = "----geckoformboundary_strawberrywashere"
FORM_SEP = f"--{FORM_BOUNDARY}\r\nContent-Disposition: form-data; name="
devlogText = "(this is a test devlog) if you're seeing this, i fiddled around with multipart forms enough to get this devlog submitted"
imageFile = b""
if len(sys.argv) > 1:
    imagePath = sys.argv[1]
else:
    imagePath = "csrf_token.png" #testing placeholder image
with open(imagePath,"rb") as file:
    imageFile = file.read()
imageExt = os.path.splitext(imagePath)[1]
imageName = os.path.basename(imagePath)
print(imageFile)
print(f"\n\n=====\n\n")
FORM_ENTRIES = {"authenticity_token": authenticity,
                "devlog[use_hackatime]":"true",
                "devlog[text]":devlogText,
                "devlog[file]": imageFile,
                "devlog[project_id]": PROJECT_ID,
                "button": ""}
requestContent = FORM_SEP
IMAGE_CONTENT = f"; filename=\"{imageName}\"\r\nContent-Type: image/{imageExt}"
for key,value in FORM_ENTRIES:
    requestContent += f"\"{key}\"\r\n\r\n{value}\r\n"


