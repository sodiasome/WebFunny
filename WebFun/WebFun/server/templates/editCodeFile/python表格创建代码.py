import pandas as pd
import sys
import xlsxwriter

path = sys.argv[1]

if ".csv" in path:
	data_dic = {"����":[18,19,20],"����":["a","b","c"]}
	csvDf = pd.DataFrame(data_dic)
	csvDf.to_csv(path,index=False,sep=',',encoding='utf_8_sig')
elif ".xlsx" in path:
	# ͨ���ֵ�ķ�ʽд�����ݣ���Ϊ�ֶΣ�ֵΪֵ
	df=pd.DataFrame({'name':['meat','rice'],'price':[12,3],'quantity':[10,100]})
	#����xlsx�ļ���
	workbook=xlsxwriter.Workbook(path)
	# ������������
	worksheet=workbook.add_worksheet()

	# ���õ�Ԫ���ʽ��
	#  ����Ӵ֣���ɫ��������ɫ����
	format_columname=workbook.add_format({'bold':True,'font_color':'blue','bg_color':'purple'}) 
	#���ü۸����ֵ��ʽ��������»���
	format_price=workbook.add_format({'num_format': '$#,##0','underline':True})
	#��������
	format_products=workbook.add_format({'font_name':'Times New Roman'})

	#��������д�����ݡ�
	#worksheet.write����д���һ�������������ֱ��ʾ�С��С����ݡ����ݸ�ʽ��
	for col in range(len(df.columns)):
		worksheet.write(0,col,df.columns[col],format_columname)
	#�ֱ�д��Ԫ�ء�
	for row in range(2):
		worksheet.write(row+1,0,df.name[row])   
	for row in range(2):
		worksheet.write(row + 1, 1, df.price[row],format_price)   
	for row in range(2):
		worksheet.write(row + 1, 2, df.quantity[row],format_products)  

	workbook.close()