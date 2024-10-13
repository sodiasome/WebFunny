
class MysqlCtl():
    
    def __init__(self):
        pass

    #def Get_TableData(self,table_node)->list[tuple]:
    #    '''从mysql查取任意一个表格数据'''
    #    return table_node.query.all()

    def Get_TableData_ByFilter(self,table_node,key,value:str):
        '''按条件查询（这是个通用的函数）'''
        try:
            if key == table_node.Date:
                return table_node.query.filter_by(Date=value).all()
        except:
            pass

        try:
            if key == table_node.producName:
                return table_node.query.filter_by(producName=value).all()
        except:
            pass

        try:
            if key == table_node.strategyName:
                return table_node.query.filter_by(strategyName=value).all()
        except:
            pass

    def Get_TableData_Last(self,table_node:any):
        '''获取最后一条数据'''
        lastData = table_node.query.all()
        if lastData:
            return lastData[-1]
        return []
