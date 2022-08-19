from cProfile import label
from cgi import test
from flask import Flask
from GetJPTime import GetJPTime
from AddLog import AddLog
import time
import multiprocessing


app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn

line_bot_api = LineBotApi('nmY3py0ibVLqXvo+X8qXxeepFtE6fXqDnOLHtEa5o1c4A8trgfXn04p0YDmleStVoGtOTOYdHNY9ZsMcsTfdcKIs18fsfSk+MXNgp/FI02mEhFwom7tL7tunBsixsB74tNMWYeKdAoGmcNevT8H/lQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bf37792da9b27fac742e418094a6cffb')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    gettext = event.message.text
    
    # --------------------需要確認-------------------------------
    if gettext == '1':
        sendConfirm(event)
        
    elif gettext == '飲んだー':
        OK(event)
        
    elif gettext == 'まだー':
        mada(event)
        

def sendConfirm(event):
    try:

        message = TemplateSendMessage(
            alt_text="確認",
            template = ConfirmTemplate(
                text="薬は、飲みましたか？",
                actions=[
                    MessageTemplateAction(
                        label='飲んだー',
                        text="飲んだー"
                    ),
                    MessageTemplateAction(
                        label='まだー',
                        text="まだー"
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エーラです"))

def OK(event):
    try:
        # 取得使用者名稱-----------------------------
        UserId = event.source.user_id
        profile = line_bot_api.get_profile(UserId)
        # ------------------------------------------
        AddLog(profile.display_name,"True")
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="了解です"))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エーラです"))

def mada(event):
    try:
        # 取得使用者名稱-----------------------------
        UserId = event.source.user_id
        profile = line_bot_api.get_profile(UserId)
        # ------------------------------------------
        AddLog(profile.display_name,"False")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="忘れないように飲んでください"))
        

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エーラです"))


def checkTime():
    line_bot_api.broadcast(TextSendMessage(text="ロボット 起動"))
    message = TemplateSendMessage(
            alt_text="確認",
            template = ConfirmTemplate(
                text="薬は、飲みましたか？",
                actions=[
                    MessageTemplateAction(
                        label='飲んだー',
                        text="飲んだー"
                    ),
                    MessageTemplateAction(
                        label='まだー',
                        text="まだー"
                    )
                ]
            )
        )
    
    while True:
        if GetJPTime() == "09:00:00" or GetJPTime() == "21:00:00":
            line_bot_api.broadcast(message)
            time.sleep(3)



def start():
    app.run()

if __name__ == '__main__':
    
    t = multiprocessing.Process(target=checkTime)
    t.start()
    t = multiprocessing.Process(target=start)
    t.start()
    


