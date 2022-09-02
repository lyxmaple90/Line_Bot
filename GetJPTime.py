from GetJPDateTime import GetJPDateTime

def GetJPTime():
    time = GetJPDateTime()
    time = time.split(" ")[1]
    return time

