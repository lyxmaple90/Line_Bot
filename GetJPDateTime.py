from datetime import datetime,timezone,timedelta

def GetJPDateTime():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=9))) # 轉換時區

    time = dt2.strftime("%Y-%m-%d %H:%M:%S")
    
    return time
    


    
