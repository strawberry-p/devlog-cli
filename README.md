## devlog-cli

CLI tool intended for posting Summer of Making devlogs from the terminal.

### Usage

**ensure you have a `session.json` file in the same folder before running this**

1. go to SoM logged in and open devlogs
2. run `document.cookie` in the console and copy the result
3. open `session.json` in the editor of your choice. for each cookie in your document.cookie result, make a new entry in the json:
`{"_journey_session": "[your session cookie here],"ahoy_visitor": "[random]", "ahoy_visit":"[also random]}`

### Options


`py devlog.py PROJECT_ID imagePath [--devlog-file] [-k]`

- PROJECT_ID - copied from project URL
- imagePath - points to the accompanying image to be sent with your devlog
- --devlog-file - points to a text file for the devlog text. if not present, ask for devlog content interactively
- --keep_name - specifies whether the server should know the image's original name, or a randomly generated curve