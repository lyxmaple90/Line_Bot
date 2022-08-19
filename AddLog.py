import pymysql.cursors
import GetJPDateTime

def AddLog(User,Answer):
    db_settings = {
        "host": "db-mysql-sgp1-64164-do-user-12125624-0.b.db.ondigitalocean.com",
        "port": 25060,
        "user": "doadmin",
        "password": "AVNS_EzPmmVy0LA0jjceHEob",
        "db": "Pallet",
        "charset": "utf8"
    }
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            sql = "insert into lineBotLog(User,Verify,Date)values(%s,%s,%s)"
            
            cursor.execute(sql,(User,Answer,GetJPDateTime.GetJPDateTime()))
            
        conn.commit()
        conn.close()
        return True

    except Exception as ex:
        print(ex)
        return False

print(AddLog('User','Answer'))