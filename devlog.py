import requests as r
from bs4 import BeautifulSoup
import json
import sys, os, random, string
PROJECT_ID = "13052"
PROJECT_PREFIX = "https://summer.hackclub.com/projects/"
USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0"
RANDOM_CHARSET = string.ascii_lowercase+string.digits+string.ascii_uppercase
FORM_BOUNDARY = "----geckoformboundary_strawberrywashere_"
FORM_BOUNDARY += ''.join(random.sample(RANDOM_CHARSET,6))
FORM_SEP = f"--{FORM_BOUNDARY}\r\nContent-Disposition: form-data; name="
with open("session.json") as session_file:
    session_cookies = json.load(session_file)
if True:
    cookie = ""
    for key,value in session_cookies.items():
        cookie += f"{key}={value};"
    cookie = cookie[:-1]
else:
    cookie = f"_journey_session={session_cookies["_journey_session"]}"
s = r.Session()
s.headers.update({"Cookie":cookie})
authenticity = ""
csrfToken = ""
def get_tokens():
    global authenticity, csrfToken
    page_html = s.get(f"{PROJECT_PREFIX}{PROJECT_ID}")
    soup = BeautifulSoup(page_html.text,"html.parser")
    formParent = soup.find_all("form",attrs={"data-controller": "form devlog-attachment-paste"})[0]
    authenticity = formParent.find("input",attrs={"name":"authenticity_token"})["value"]
    csrfToken = soup.find("meta",attrs={"name":"csrf-token"})["content"]
    print(authenticity)
    print(csrfToken)
    return((authenticity, csrfToken))
s_devlog = r.Session()
s_devlog.headers.update({"Cookie": cookie}) #can't add the authenticity csrf token, it might change
if len(sys.argv) > 2:
    imagePath = sys.argv[2]
    logPath = sys.argv[1]
elif len(sys.argv) > 1:
    imagePath = "multipart_constructed.png" #testing placeholder image
    logPath = sys.argv[1]
else:
    imagePath = "multipart_constructed.png"
    logPath = "devlog.txt"
    
requestContent = ""
def prep_req(authenticity,imagePath="multipart_constructed.png",devlogText="(this is a test devlog) if you're seeing this, i fiddled around with multipart forms enough to get this devlog submitted"):
    global requestContent, s_devlog
    imageFile = b""
    with open(imagePath,"rb") as file:
        imageFile = file.read()
    imageExt = os.path.splitext(imagePath)[1]
    imageName = os.path.basename(imagePath)
    print(imageName)
    requestContent = ""
    FORM_ENTRIES = {"authenticity_token": authenticity,
                    "devlog[use_hackatime]":"true",
                    "devlog[text]": devlogText,
                    "devlog[file]": str(imageFile)[2:-1],
                    "devlog[project_id]": PROJECT_ID,
                    "button": ""}
    #[2:-1] removes the b'' mark from conversion to text
    for key,value in FORM_ENTRIES.items():
        if key == "devlog[file]":
            imgInsert = f"; filename=\"{imageName}\"\r\nContent-Type: image/{imageExt[1:]}"
            #slicing the first character removes the dot
        else:
            imgInsert = ""
        requestContent += f"{FORM_SEP}\"{key}\"{imgInsert}\r\n\r\n{value}\r\n"
    requestContent += f"--{FORM_BOUNDARY}--"
    #print(requestContent)
    s_devlog.headers.update({"Host":"summer.hackclub.com",
                            "User-Agent": USERAGENT,
                            "Accept":"text/vnd.turbo-stream.html, text/html, application/xhtml+xml",
                            "Accept-Language": "en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br, zstd",
                            "Referer":f"{PROJECT_PREFIX}{PROJECT_ID}",
                            "x-turbo-request-id": "7a84b0c5-7899-4604-8e81-52a12d230156",
                            "Content-Type": f"multipart/form-data; boundary={FORM_BOUNDARY}",
                            "Origin": "https://summer.hackclub.com",
                            "Sec-GPC": "1",
                            "Connection":"keep-alive",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-origin",
                            "Priority": "u=0",
                            "TE": "trailers"})
def devlog_post(csrf=csrfToken,content=requestContent):
    postData = {"mimeType": f"multipart/form-data; boundary={FORM_BOUNDARY}",
                "params":[],
                "text": content}
    res = s_devlog.post(f"{PROJECT_PREFIX}{PROJECT_ID}/devlogs",data=postData, headers={"x-csrf-token":f"{csrf}"})
    return res

if __name__ == "__main__":
    get_tokens()
    with open(logPath) as file:
        logText = file.read()
    prep_req(authenticity, devlogText=f"{logText}")
    resp = devlog_post()
    print(resp.content)
    print(resp.status_code)