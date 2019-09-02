from flask import Flask, request
import json
import requests
global LINE_API_KEY
LINE_API_KEY = "Your line api key"

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is Punsikorn chatbot server.'

@app.route('/bot', methods=['POST'])
def bot():
    replyQueue = list()
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)

    replyToken = msg_in_json["events"][0]['replyToken']

    userID = msg_in_json["events"][0]['source']['userId']
    msgType = msg_in_json["events"][0]['message']['type']

    if msgType != 'text':
        reply(replyToken, ['Only text is allowed.'])
        return 'OK',200
    
    text = msg_in_json["events"][0]['message']['text'].lower().strip()
    print(text)
    response_dict = {
        'สวัสดีค่ะ':'สวัสดีค่าาา ปัญ BNK48 ค่าาาา ว่าแต่ สรุปแล้วเราต้องใช้ "ค่ะ" หรือ "คะ" กันแน่ หนูงง 555+',
        'สวัสดีครับ':'สวัสดีค่าาา ปัญ BNK48 ค่าาาา',
        'สวัสดี':'สวัสดีค่าาา น้องปัญค่าา x)'
    }
    if text in response_dict:
        print(response_dict[text])
        replyQueue.append(response_dict[text])
    else:
        replyQueue.append('หนูไม่รู้จะตอบไรเลยค่าาาาาา 555+')
    
    # replyQueue.append('นี่คือรูปแบบข้อความที่รับส่ง')
    # replyQueue.append(msg_in_string)
    reply(replyToken, replyQueue)
    return 'OK',200

def reply(replyToken, textList):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text": text
        })
    data = json.dumps({
        "replyToken": replyToken,
        "messages": msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return

if __name__ == '__main__':
    app.run()
