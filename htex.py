import argparse
import urllib.request
import re

parser = argparse.ArgumentParser(
    prog="htex",
    description="scrapes html from a webpage",
    epilog="epilog"
)

# url
parser.add_argument(
    "url", 
    help="The URL or URI to pull HTML from."
)
# custom regex file
parser.add_argument(
    "regexfile", 
    help="The file containing the RegEx to perform on the HTML."
)
# remove all javascript
parser.add_argument(
    "-njs", "--nojavascript", 
    help="Use to ignore JavaScript in the source HTML.",
    action="store_true"
)
# use https (http by default)
parser.add_argument(
    "-s", "--https", 
    help="Use HTTPS rather than default HTTP.",
    action="store_true"
)
# return all html first
parser.add_argument(
    "-a", "--all", 
    help="Display all HTML (subject to -njs).",
    action="store_true"
)

# parse args
args = parser.parse_args()

url = args.url

prefix = "http://"
if (args.https): prefix = "https://"
url = prefix + url

regex = []

if (args.regexfile != ""):
    file = open(args.regexfile, "r")
    regex = file.readlines()
    file.close()

# request
req = urllib.request.Request(url, headers={"Accept":"*/*","User-Agent":"a"})
# response
resp = urllib.request.urlopen(req)

content = resp.read().decode(resp.headers.get_content_charset())
ret = ""

js_regex = r"<script.*?>[.\S\s]*?</script>"

if (args.nojavascript):
    content = "".join(re.split(js_regex, content))

if (args.all):
    ret += content

pattern_matches = {}

for pattern in regex:
    pattern = pattern.rstrip()
    matches = re.findall(pattern, content)
    pattern_matches[pattern] = set(matches)

for pattern in pattern_matches:
    pattern = pattern.rstrip()
    ret += "\n\n"+pattern+"  :\n"
    for match in pattern_matches[pattern]:
        ret += "\t"+match+"\n"

print(ret)