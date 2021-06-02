#!/usr/bin/env python3
"""Example bot that returns a synchronous response."""

from flask import Flask, request, json
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

scopes = 'https://www.googleapis.com/auth/chat.bot'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'bot_info/ranking-bot-315505-c5befdb30556.json', scopes)

chat_service = build('chat', 'v1', http=credentials.authorize(Http()))



app = Flask(__name__)


@app.route('/', methods=['POST'])
def on_event():
  """Handles an event from Google Chat."""
  event = request.get_json()
  if event['type'] == 'ADDED_TO_SPACE' and not event['space']['singleUserBotDm']:
    text = 'Thanks for adding me to "%s"!' % (event['space']['displayName'] if event['space']['displayName'] else 'this chat')
  elif event['type'] == 'MESSAGE':
    text = 'You said: `%s`' % event['message']['text']
  else:
    return
  return json.jsonify({'text': str(event)}) # json.jsonify({'text': text})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=False)