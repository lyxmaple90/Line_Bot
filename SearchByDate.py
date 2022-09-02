

import pymysql.cursors


def SearchByDate(UserID,Date):
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

        

        # del RowResult
        DBList = []

        for i in RowResult:
            list = [i[0],i[1],i[2].strftime("%Y/%m/%d, %H:%M:%S")]
            DBList.append(list)
        
        ResultList = []
        for i in DBList:
            if str(i[2]).split(",")[0] == Date:
                ResultList.append(i)


        Result = f"{ResultList[0][0]}さん :"
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
        return "この日は記録ありません"



