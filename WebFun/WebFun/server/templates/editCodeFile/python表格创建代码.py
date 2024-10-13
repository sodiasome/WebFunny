import pandas as pd
import sys
import xlsxwriter

path = sys.argv[1]

if ".csv" in path:
	data_dic = {"年龄":[18,19,20],"名字":["a","b","c"]}
	csvDf = pd.DataFrame(data_dic)
	csvDf.to_csv(path,index=False,sep=',',encoding='utf_8_sig')
elif ".xlsx" in path:
	# 通过字典的方式写入数据，键为字段，值为值
	df=pd.DataFrame({'name':['meat','rice'],'price':[12,3],'quantity':[10,100]})
	#创建xlsx文件。
	workbook=xlsxwriter.Workbook(path)
	# 新增工作簿。
	worksheet=workbook.add_worksheet()

	# 设置单元格格式。
	#  字体加粗，蓝色背景，紫色背景
	format_columname=workbook.add_format({'bold':True,'font_color':'blue','bg_color':'purple'}) 
	#设置价格的数值格式，并添加下划线
	format_price=workbook.add_format({'num_format': '$#,##0','underline':True})
	#设置字体
	format_products=workbook.add_format({'font_name':'Times New Roman'})

	#向工作表中写入数据。
	#worksheet.write函数写入第一行列名，参数分别表示行、列、数据、数据格式。
	for col in range(len(df.columns)):
		worksheet.write(0,col,df.columns[col],format_columname)
	#分别写入元素。
	for row in range(2):
		worksheet.write(row+1,0,df.name[row])   
	for row in range(2):
		worksheet.write(row + 1, 1, df.price[row],format_price)   
	for row in range(2):
		worksheet.write(row + 1, 2, df.quantity[row],format_products)  

	workbook.close()