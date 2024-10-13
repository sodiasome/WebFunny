
from threading import Timer
import time
import os


class LastUpload():
    def __init__(self,strForder):
        self.nFileIndex = 1#�ڼ����ļ�
        self.mapFile = {}#ͨ��id�ҵ��ļ���
        self.bFirstRun = True#�����һ������
        self.nHisSize = 0
        self.strForder = strForder
        self.strConfig = "./config.txt"

    def IterForder(self,forder:str):
        '''�ݹ�����ļ�'''
        for root,dirs,files in os.walk(forder):
            if files:
                for file in files:
                    #��ȡ�ļ���
                    names = file.split(".")

                    if names[1] in self.mapFile.values():# ��ͬĿ¼��ͬ���ļ�����
                        continue

                    self.mapFile[str(self.nFileIndex)] = names[1]
                    self.nFileIndex += 1
            if dirs:
                for dir in dirs:
                    self.IterForder(forder + '/' +dir)

    def GetHistoryConfig(self):
        '''��ȡ��ʷ�ļ�'''
        historyFile = []
        if os.path.exists(self.strConfig):
            with open(self.strConfig,"r") as fp:
                lines = fp.readlines()
                for line in lines:
                    row = line.split(' ')
                    historyFile.append(row[1])
        else:
            with open(self.strConfig,"w")as fp:
                pass
        return historyFile

    def SaveConfig(self):
        '''�������ϴ����ļ�'''  
        #�����޸��ļ�����ɾ���ļ� bug
        hisFile:list = self.GetHistoryConfig()
        addCount = len(hisFile) + 1
        with open(self.strConfig,"a") as fp:
            for index,file in self.mapFile.items():
                if not hisFile and not file in hisFile:
                    time.gmtime(time.time())
                    strTime = time.strftime('%Y/%m/%d/%H:%M:%S', time.gmtime(time.time()))

                    strRow = strTime+' '+file+' '+str(addCount) + "\n"
                    fp.write(strRow)

                    addCount += 1


    def GetHisSize(self)->int:
        '''��ȡ��ʷ�ļ�����'''
        self.bFirstRun = False
        nHisSize = 0
        with open(self.strConfig,"r") as fp:
            lines = fp.readlines()
            lastLine = lines[-1]
            nHisSize = int(lastLine.split(' ')[2])
        return nHisSize

    def WorkThread(self):
        self.IterForder(self.strForder)

        if self.nFileIndex != self.nHisSize:
            self.SaveConfig()#�������ϴ����ļ���¼�������ļ���

        if self.bFirstRun:
            self.nHisSize = self.GetHisSize()

        self.LoopTimer()

    def LoopTimer(self):
        if self.bFirstRun:
            Timer(0,self.WorkThread).start()
        else:
            Timer(10,self.WorkThread).start()

    def GetLastFiles(self)->list:
        '''��ȡ�����ϴ����ļ�'''
        uploadTime = ""
        lastFiles = []
        with open(self.strConfig,"r") as fp:
            lines = fp.readlines()
            for row in lines:
                strRow = row.split(' ')

                if uploadTime != strRow[0]:
                    uploadTime = strRow[0]
                    lastFiles = []
                lastFiles.append(strRow[1])

        return lastFiles

    def GetNameById(self,id:str):
        return self.mapFile[id]

if __name__ == "__main__":
    print("��ʱ�߳��Ѿ����.")
    lastUpload = LastUpload("./test")
    lastUpload.LoopTimer()
    time.sleep(2)
    print(lastUpload.GetLastFiles())
    print(lastUpload.GetNameById("1"))

