from flask import Flask,render_template
from GetJPTime import GetJPTime
from AddLog import AddLog
from SearchAll import SearchAll
from GetJPDateTime import GetJPDateTime
from SearchByDate import SearchByDate

import os
from urllib.parse import parse_qsl

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, PostbackTemplateAction, DatetimePickerTemplateAction,ButtonsTemplate,PostbackEvent

app = Flask(__name__)

line_bot_api = LineBotApi('61r/mO0+uhN0io7/R0OnGZb5m3O7ED0Qr+s9xsijsYfvbRD+CdLmnasEwxxylaT5oGtOTOYdHNY9ZsMcsTfdcKIs18fsfSk+MXNgp/FI02m2yS8PvHUm3LR4x8mzVJqxzqqagFLQC145teKSw6+1mQdB04t89/1O/w1cDnyilFU=')
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
    
    
    if gettext == '1':
        sendConfirm(event)

    elif gettext == '飲んだー':
        OK(event)
        
    elif gettext == 'まだー':
        mada(event)
    elif gettext == '2':
        time = GetJPTime()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=time))
    elif gettext == '日にちで検索':
        SomeDayRecord(event)
    elif gettext == '全部の記録':  
        History(event)

def SomeDayRecord(event):
    
    try:
        message = TemplateSendMessage(
            alt_text='日にちで検索',
            template=ButtonsTemplate(
                
                
                text='日にちで検索',
                actions=[
                    DatetimePickerTemplateAction(
                        label="日にちを選ぶ",
                        data="action=sell&mode=date",  #觸發postback事件
                        mode="date",  #選取日期
                        initial=GetJPDateTime().split(" ")[0],  #顯示初始日期
                        min="2022-01-01",  #最小日期
                        max="2100-12-31"  #最大日期
                    
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='エーラです'))

@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  #取得data資料
    if backdata.get('action') == 'sell':
        sendData_sell(event, backdata)


def sendData_sell(event, backdata):  #Postback,顯示日期時間
    # 取得使用者名稱-----------------------------
    UserId = event.source.user_id
    
    # ------------------------------------------
    try:
        if backdata.get('mode') == 'date':
            dt =  str(event.postback.params.get('date'))  #讀取日期
            dt = dt.replace("-", "/")
            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=SearchByDate(UserId,dt)))
            
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='エーラです'))



def History(event):
    # 取得使用者名稱-----------------------------
    UserId = event.source.user_id
    
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=SearchAll(UserId)))


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
        AddLog(profile.user_id,profile.display_name,"True")
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="了解です"))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エーラです"))

def mada(event):
    try:
        # 取得使用者名稱-----------------------------
        UserId = event.source.user_id
        profile = line_bot_api.get_profile(UserId)
        # ------------------------------------------
        AddLog(profile.user_id,profile.display_name,"False")
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="忘れないように飲んでください"))
        

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エーラです"))


     
if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    


