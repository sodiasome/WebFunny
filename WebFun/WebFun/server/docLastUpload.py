
from threading import Timer
import time
import os


class LastUpload():
    def __init__(self,strForder):
        self.nFileIndex = 0#第几个文件
        self.mapFile = {}#通过id找到文件名
        self.nHisSize = 0
        self.strForder = strForder
        self.strConfig = ".\\config.txt"
        self.timeLock = 0#定时器时间间隔

    def SetForder(self,strForder):
        self.strForder = strForder
        forders = strForder.split("\\")
        self.strConfig = strForder+"\\..\\"+forders[-1]+"Config.txt"
        #print("设置目录成功.",self.strForder)

    def IterForder(self,forder:str):
        '''递归遍历文件'''
        for root,dirs,files in os.walk(forder):
            if files:
                for file in files:
                    #提取文件名
                    names = file.split(".")

                    if names[1] in self.mapFile.values():# 不同目录，同名文件处理
                        continue

                    self.mapFile[str(names[0])] = names[1]
                    self.nFileIndex += 1
            if dirs:
                for dir in dirs:
                    self.IterForder(forder + '/' +dir)

    def GetHistoryConfig(self):
        '''获取历史文件'''
        historyFile = []
        if os.path.exists(self.strConfig):
            with open(self.strConfig,"r",encoding="utf-8",errors="ignore") as fp:
                lines = fp.readlines()
                for line in lines:
                    row = line.split(' ')
                    historyFile.append(row[1])
        else:
            pass
        return historyFile

    def SaveConfig(self):
        '''保存新上传的文件'''  
        #保存修改文件名、删除文件 bug
        hisFile:list = self.GetHistoryConfig()
        #print("新上传文件写入",self.strConfig)
        nLen = len(self.mapFile)

        with open(self.strConfig,"a",encoding="utf-8") as fp:
            for i in range(0,nLen):

                if str(i+1) in self.mapFile.keys() is False:
                    continue

                file = self.mapFile[str(i+1)]

                if not hisFile or not file in hisFile:
                    strTime = time.strftime('%Y/%m/%d/%H:%M',time.localtime())

                    strRow = strTime+' '+file+' '+str(i+1) + "\n"
                    fp.write(strRow)

    def GetHisSize(self)->int:
        '''获取历史文件数量'''
        nHisSize = 0
        print("读取文件大小：",self.strConfig)
        if os.path.exists(self.strConfig):
            with open(self.strConfig,"r",encoding="utf-8",errors="ignore") as fp:
                lines = fp.readlines()
                if lines:
                    lastLine = lines[-1]
                    nHisSize = int(lastLine.split(' ')[2])
        return nHisSize

    def WorkThread(self):
        #print("WorkThread",self.strForder)
        self.IterForder(self.strForder)

        #print(self.nFileIndex,self.nHisSize)
        #print(self.mapFile)

        if self.nFileIndex != self.nHisSize:
            self.SaveConfig()#保存新上传的文件记录到配置文件中

        self.nHisSize = self.GetHisSize()
        self.timeLock = 10
        #self.LoopTimer()

    def LoopTimer(self,bEnable:bool=False):
        Timer(self.timeLock,self.WorkThread).start()

    def GetLastFiles(self):
        '''获取最新上传的文件'''
        uploadTime = ""
        lastFiles = []

        with open(self.strConfig,"r",encoding="utf-8",errors="ignore") as fp:
            lines = fp.readlines()
            for row in lines:
                strRow = row.split(' ')

                if uploadTime != strRow[0]:
                    uploadTime = strRow[0]
                    lastFiles = []
                lastFiles.append(strRow[1])

        return lastFiles,uploadTime

    def GetNameById(self,id:str):
        if id in self.mapFile.keys():
            return self.mapFile[id]
        else:
            return ""

if __name__ == "__main__":
    print("定时线程已经启动.")
    lastUpload = LastUpload("")
    lastUpload.SetForder("E:\\tianProject\\WebFun\\WebFun\\server\\templates\\postMessage")
    #lastUpload.SetForder("E:\\tianProject\\WebFun\\WebFun\\server\\templates\\postMessage")
    lastUpload.WorkThread()
    lastFiles,uploadTime = lastUpload.GetLastFiles()
    print(lastUpload.GetNameById("2"))

