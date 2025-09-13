import requests as r
from bs4 import BeautifulSoup
import json, argparse
import sys, os, random, string
PROJECT_ID = "13052"
PROJECT_PREFIX = "https://summer.hackclub.com/projects/"
USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0"
RANDOM_CHARSET = string.ascii_lowercase+string.digits+string.ascii_uppercase
FORM_BOUNDARY = "----geckoformboundary_strawberrywashere_"
FORM_BOUNDARY += ''.join(random.sample(RANDOM_CHARSET,6))
FORM_SEP = f"--{FORM_BOUNDARY}\r\nContent-Disposition: form-data; name="
HANDROLL = False
parser = argparse.ArgumentParser(description="Post Summer of Making devlogs from the CLI")
parser.add_argument("PROJECT_ID")
parser.add_argument("imagePath",help="path to image file from the working dir",type=str)
parser.add_argument("-d","--devlog-file",default=False,help="path to text file to post as devlog from the working dir")
parser.add_argument("-k","--keep-name",action="store_true",help="do not rename devlog image")
args = parser.parse_args()
PROJECT_ID = args.PROJECT_ID
if not os.path.isfile("session.json"):
    print("\r\n! you do not have a session.json file, please check the README for the instructions to include your SoM cookies !\r\n")
    raise Exception


with open("session.json") as session_file:
    try:
        session_cookies = json.load(session_file)
    except json.JSONDecodeError as _:
        print("\r\n! malformed JSON, make sure session.json is valid JSON !\r\n")
        raise _
if not args.devlog_file:
    devText = input("write a devlog\n")
else:
    with open(args.devlog_file,"rt") as file:
        devText = file.read()
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
FORM_ENTRIES = {}    
requestContent = ""
imageFile = b""
imageName = f"devlog_{PROJECT_ID}_{''.join(random.sample(RANDOM_CHARSET,8))}"
imageExt = ""
def prep_req(authenticity,imagePath,devlogText):
    global requestContent, s_devlog, FORM_ENTRIES, imageFile, imageName, imageExt
    imageFile = b""
    with open(imagePath,"rb") as file:
        imageFile = file.read()
    imageExt = os.path.splitext(imagePath)[1][1:]
    if args.keep_name:
        imageName = os.path.basename(imagePath)
    print(imageName)
    FORM_ENTRIES = {"authenticity_token": authenticity,
                    "devlog[use_hackatime]":"true",
                    "devlog[text]": devlogText,
                    "devlog[file]": str(imageFile)[2:-1],
                    "devlog[project_id]": PROJECT_ID,
                    "button": ""}
    #[2:-1] removes the b'' mark from conversion to text
    if HANDROLL:
        requestContent = ""
        for key,value in FORM_ENTRIES.items():
            if key == "devlog[file]":
                imgInsert = f"; filename=\"{imageName}\"\r\nContent-Type: image/{imageExt}"
                #slicing the first character removes the dot
            else:
                imgInsert = ""
            requestContent += f"{FORM_SEP}\"{key}\"{imgInsert}\r\n\r\n{value}\r\n"
        requestContent += f"--{FORM_BOUNDARY}--"
        #print(requestContent)
    else:
        del FORM_ENTRIES["devlog[file]"]

    s_devlog.headers.update({"Host":"summer.hackclub.com",
                            "User-Agent": USERAGENT,
                            "Accept":"text/vnd.turbo-stream.html, text/html, application/xhtml+xml",
                            "Accept-Language": "en-US;q=0.5,en;q=0.3",
                            "Accept-Encoding": "gzip, deflate, br, zstd",
                            "Referer":f"{PROJECT_PREFIX}{PROJECT_ID}",
                            "x-turbo-request-id": "7a84b0c5-7899-4604-8e81-52a12d230156",
                            "Origin": "https://summer.hackclub.com",
                            "Sec-GPC": "1",
                            "Connection":"keep-alive",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-origin",
                            "Priority": "u=0",
                            "TE": "trailers"})
def devlog_post(csrf=csrfToken,content=FORM_ENTRIES):
    #postData = {"mimeType": f"multipart/form-data; boundary={FORM_BOUNDARY}",
    #            "params":[],
    #            "text": content}
    if (imageExt) and (imageExt != "") and (imageExt != "mp4"):
        fileTuple = (imageName,imageFile,f"image/{imageExt}")
    else:
        fileTuple = (imageName,imageFile)
    if True:
        req = r.Request("POST",f"{PROJECT_PREFIX}{PROJECT_ID}/devlogs",data=content,files={"devlog[file]": fileTuple},headers={"x-csrf-token": f"{csrf}"})
        print(req.headers)
        print("^^ OG headers")
        prepared_req = s_devlog.prepare_request(req)
        #print(prepared_req.headers)
        try:
            print("body:")
            #print(prepared_req.body[:400])
        except Exception as _:
            print(f"weh {_}")
        res = s_devlog.send(prepared_req, timeout=10, allow_redirects=False)
    else:
        res = s_devlog.post(f"{PROJECT_PREFIX}{PROJECT_ID}/devlogs",data=content, files={"devlog[file]": fileTuple}, headers={"x-csrf-token":f"{csrf}"})
    
    return res

if __name__ == "__main__":
    get_tokens()
    #with open(logPath) as file:
        #logText = file.read()
    #prep_req(authenticity, devlogText=f"{logText}")
    prep_req(authenticity,args.imagePath,devText)
    #print(requestContent[:200])
    print("=== devlog_post ===")
    print(FORM_ENTRIES)
    resp = devlog_post(csrf=csrfToken,content=FORM_ENTRIES)
    print(resp.status_code)