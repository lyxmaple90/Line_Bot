
import pymysql.cursors


def SearchAll(UserID):
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
            sql = "select User,Verify,Date from lineBotLog where UserID = %s"
            
            cursor.execute(sql,(UserID))
            DBResult = cursor.fetchall()


        conn.commit()
        conn.close()

        RowResult = []
        for i in DBResult:
            RowResult.append(i)

        ResultList = []

        for i in RowResult:
            list = [i[0],i[1],i[2].strftime("%Y/%m/%d, %H:%M:%S")]
            ResultList.append(list)

        del RowResult
        Result = f"{ResultList[0][0]}さん:"
        for i in ResultList:
            if i[1] == "True":
                # Date = i[2].strftime("%Y/%m/%d, %H:%M:%S")
                Result += f"\n{i[2]}\n飲みました"
            elif i[1] == "False":
                # Date = i[2].strftime("%Y/%m/%d, %H:%M:%S")
                Result += f"\n{i[2]}\n飲んでなかった"
        return Result
        

    except Exception as ex:
        print(ex)
        return False



