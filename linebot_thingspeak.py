from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

app = Flask(__name__)

# Line Bot 設定
channel_secret = 9500de1d878fd1cdc553c3427082dd6e 'YOUR_CHANNEL_SECRET'
channel_access_token = 0Jg/QduwGWlSL6GUBUo8+4hLfl/tdVRWID++0/rdqBsv4xQbsyBflpq/kFbwCPiJi31csB/wjlB1bbp47FYMDN9M6rIe+diTqL+mVimp9zKUjLSvHRt/e/A66tSYDYqkfJSmREerPhyZkyZ4nSUcPgdB04t89/1O/w1cDnyilFU= 'YOUR_CHANNEL_ACCESS_TOKEN'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# ThingSpeak 設定
thingspeak_channel_id = 1120124 'YOUR_THINGSPEAK_CHANNEL_ID'
thingspeak_read_api_key = 8W7FA0AV6RZQ6R3X 'YOUR_THINGSPEAK_READ_API_KEY'

# 處理 Line Bot 訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.lower() == 'get value':
        value = get_thingspeak_value()
        reply_message = f"ThingSpeak Value: {value}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

# 從 ThingSpeak 讀取數值
def get_thingspeak_value():
    url = f"https://api.thingspeak.com/channels/{thingspeak_channel_id}/fields/1.json?api_key={thingspeak_read_api_key}&results=1"
    response = requests.get(url)
    data = response.json()
    if 'feeds' in data and len(data['feeds']) > 0:
        value = data['feeds'][0]['field1']
        return value
    return "No data available"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run()
