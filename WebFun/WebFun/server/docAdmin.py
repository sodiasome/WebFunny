# 账户管理
from mysql.mysqlCtl import MysqlCtl
from server.struct import User



class Admin():
    def __init__(self):
        self.dicAdmin = {}#用户信息
        self.mysqlCtl = MysqlCtl()

        self.Update()#初始化

    def Update(self):
        '''更新数据'''
        self.ReadAdmin()

    def ReadAdmin(self):
        '''读取所有用户信息'''
        
        tb_nodes:list = User.query.all()
        for node in tb_nodes:
            user = User()
            user.id = str(vars(node)["id"])
            user.name = vars(node)["name"]
            user.passwd = str(vars(node)["passwd"])
            self.dicAdmin[user.name] = node

            #print(user.name,user.passwd)



           

