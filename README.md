## devlog-cli

CLI tool intended for posting Summer of Making devlogs from the terminal.

## Installation

Python:

1. download `devlog.py`
2. run `pip install -r requirements.txt` in the same directory
(possibly use `pip3` if `pip` is pip2 on your machine)
3. add your SoM session cookies to `session.json` in the same directory as described below

Pyinstaller build:

1. download `dist/devlog/devlog.exe`
2. add your SoM session cookies to `session.json`

### Session

**ensure you have a `session.json` file in the same folder before running this:**

1. go to [SoM](https://summer.hackclub.com/my_projects) while logged in and open developer tools.
2. run `document.cookie` in the console and copy the result. make sure you copied the entire cookie value. (alternatively, you can use cookie manipulation extensions)
3. open `session.json` in the editor of your choice. for each cookie in your document.cookie result, make a new entry in the json:
`{"_journey_session": "[your session cookie here],
"ahoy_visitor": "[bleh]",
"ahoy_visit":"[also bleh]"}`
("_journey_session" is the only crucial cookie there, and has to be copied completely)

## Usage

1. (optional) write your devlog in a text file and save it in the same directory as devlog.py
2. save the devlog screenshot/video (video not verified to work yet) in the same directory
3. copy your current project's ID
4. run `py devlog.py PROJECT_ID /path/to/image --devlog-file /path/to/devlog`

### Options


`py devlog.py PROJECT_ID imagePath [--devlog-file /path/to/devlog] [-k]`

- PROJECT_ID - copied from project URL
- imagePath - points to the accompanying image to be sent with your devlog
- --devlog-file - points to a text file for the devlog text. if not present, asks for devlog content interactively
- --keep_name - specifies whether the server should know the image's original name, or a randomly generated curve