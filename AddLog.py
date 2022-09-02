import pymysql.cursors
import GetJPDateTime

def AddLog(UserID,User,Answer):
    db_settings = {
        "host": "xxxxxxxxxxxxxxx",
        "port": xxxxxxxxxxxxxxx,
        "user": "xxxxxxxxxxxxxxx",
        "password": "xxxxxxxxxxxxxxx",
        "db": "xxxxxxxxxxxxxxx",
        "charset": "utf8"
    }
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            sql = "insert into lineBotLog(UserID,User,Verify,Date)values(%s,%s,%s,%s)"
            
            cursor.execute(sql,(UserID,User,Answer,GetJPDateTime.GetJPDateTime()))
            
        conn.commit()
        conn.close()
        return True

    except Exception as ex:
        print(ex)
        return False

