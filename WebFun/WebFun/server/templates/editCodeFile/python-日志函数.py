import time
import os

def WriteRunLog(strLog):
    '''写入日志文件'''
    logForder = "./RunLog/"

    file = time.strftime("%Y%m%d",time.localtime())
    logFile = logForder + file + ".txt"

    ct = time.time()
    currTime = time.strftime("%Y/%m/%d/%H:%M:%S",time.localtime(ct))
    secs = (ct-int(ct))*1000
    secsTime = "%s.%03d"%(currTime,secs)
    logLine = secsTime + "\t" + strLog + "\n"

    if not os.path.exists(logForder):
        os.makedirs(logForder)

    if not os.path.exists(logFile):
        with open(logFile,"w",encoding='utf-8')as fp:
            fp.write(logLine)
    else:
        with open(logFile,"a",encoding='utf-8')as fp:
            fp.write(logLine)

for i in range(0,10):
    WriteRunLog("日志写入")