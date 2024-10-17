import urllib.request, os
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
foundLinks = []
flagFile = "notifiedFlag"

def sendSlackMessage(msg):
  slack_token = os.environ["SLACK_BOT_TOKEN"]
  slack_channel = os.environ["SLACK_CHANNEL"]
  client = WebClient(token=slack_token)
  myChannel = slack_channel

  try:
      client.chat_postMessage(
          channel=myChannel,
          text=msg
        )
  except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      print(e.response)    # str like 'invalid_auth', 'channel_not_found'

def writeFlag():
   open(flagFile, 'a').close()

def removeFlag():
  os.remove(flagFile)

def flagged():
   return os.path.isfile(flagFile)

ourUrl = os.environ["URL_TO_WATCH"]
ourString = os.environ["STRING_TO_LOOK_FOR"]

contents = urllib.request.urlopen(ourUrl).read()
soup = BeautifulSoup(contents, features="html.parser")

links = soup.find_all('a')
for l in links:
  if ourString in str.lower(l.get('href')):
    # print(l)
    foundLinks.append(l)

if len(foundLinks) > 0:
  if not flagged():
    sendSlackMessage(ourString + " : string found !!!")
    for l in foundLinks:
      sendSlackMessage(str(l))
    writeFlag()
else:
  if flagged():
    sendSlackMessage(ourString + " : string removed. Will notify again if found.")
    removeFlag()

# print(contents)