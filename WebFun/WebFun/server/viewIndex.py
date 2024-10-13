# -*- coding: utf-8 -*-
#==================================================
#	Project Name: server
#	File Name	: __init__.py
#	Author		: HuangDaTian
#	Create Time	: 2022-03-13  9:26:07
#	Modify Time	: 2022-03-13  9:26:07
#	Description	: 
#==================================================*/
from flask import Flask,flash
from flask import render_template, redirect, url_for, request
from server import app
from flask import render_template,url_for
from flask import Blueprint
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask import session
import os
import simplejson
from datetime import datetime
import time

from server.struct import User
from server.struct import RegisterForm
from server.struct import LoginForm
from server.docAdmin import Admin
from server.struct import db
from server.docLastUpload import LastUpload

app.config["WTF_CSRF_ENABLED"] = False
app.secret_key = os.urandom(24)            # cookie
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '你必须登陆后才能访问该页面'
login_manager.login_message_category = "info"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0# 禁止缓存 0s

g_codeLock = "11235813213455"

indexBp = Blueprint('IndexBp',__name__,template_folder='templates',static_folder='static')

g_lastUpload = LastUpload("")
g_lastPrivate = LastUpload("")

def GetWorkRoot():
    privateDir = "postMessage"
    workDir = "E:\\tianProject\\WebFun\\WebFun\\server\\templates\\postMessage"

    if "online" in session and  session["online"] != "":
        workDir = "E:\\tianProject\\WebFun\\WebFun\\server\\templates\\postPrivate"
        privateDir = "postPrivate"
    return workDir,privateDir

def WriteRunLog(strLog):
    '''写入日志文件'''
    logForder = ".\\RunLog\\"

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
        with open(logFile,"w",encoding='utf-8',errors="ignore")as fp:
            fp.write(logLine)
    else:
        with open(logFile,"a",encoding='utf-8',errors="ignore")as fp:
            fp.write(logLine)

def ReqRunLog(strReq):
    ip = request.remote_addr
    method = request.method
    WriteRunLog(ip+"\t"+method+"\t"+strReq)

@login_manager.user_loader  
def load_user(user_id):
    pass

@indexBp.route('/')
@indexBp.route('/Index',methods=['POST','GET'])
def Index():
    ReqRunLog("Index")
    return render_template(
        'index.html',
        register=url_for("IndexBp.register"),
        login=url_for("IndexBp.login"),
        about=url_for("IndexBp.About"),
        )

#@indexBp.route('/')
@indexBp.route('/System',methods=['POST','GET'])
#@login_required
def System():
    #return render_template(
    #    'system/system.html',
    #    user = "debug",
    #    account = "#",
    #    login_out = url_for("IndexBp.logout"),
    #)

    if "online" in session and session["online"] != "":
        ReqRunLog(session["online"]+"\t"+"System")
        return render_template(
            'system/system.html',
            user = session["online"],
            account = "#",
            login_out = url_for("IndexBp.logout"),
            user_name = session["online"],
            user_ip = request.remote_addr,
            user_regeditTime = "null",
            user_lastTime = "null",
            user_sumTime = "null",
            )   
    else:
        ReqRunLog("System")
        return redirect(url_for('IndexBp.error'))
                

@indexBp.route('/About',methods=['POST','GET'])
def About():
    ReqRunLog("About")
    return render_template(
        'about.html'
        )


@indexBp.route('/register',methods=['GET','POST'])
def register():
    '''注册初始化'''
    ReqRunLog("register")
    register_form = RegisterForm()
    return render_template(
        'register.html',
        form = register_form
        ) 

@indexBp.route('/login',methods=['GET','POST'])
def login():
    '''登录初始化'''
    ReqRunLog("login")
    login_form = LoginForm()
    return render_template(
        'login.html',
        form = login_form
        ) 

@indexBp.route('/logout',methods=['GET','POST'])
#@login_required
def logout():
    '''退出登录'''
    if "online" in session and  session["online"] != "":
        ReqRunLog(session["online"]+"\t"+"logout")
        #logout_user() 
        session["online"] = ""
        return redirect(url_for('IndexBp.Index'))
    else:
        ReqRunLog("logout")
        return redirect(url_for('IndexBp.error'))

@indexBp.route('/LoginCtl',methods=['GET','POST'])
def LoginCtl():
    '''登录表单验证'''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        curr_user = User()

        #判断用户是否存在
        adminCtl = Admin()
       
        #print(form.data["username"])
        name = form.data["username"]
        passwd = form.data["password"]
        if name in adminCtl.dicAdmin.keys():
            node:User = adminCtl.dicAdmin[name]
            if node.check_password(node.passwd,passwd):
                #print("登录成功.")
                #login_user(curr_user)# 记录登录用户
                session["online"] = name
                ReqRunLog(session["online"]+"\t"+"LoginCtl")
                return redirect(url_for('IndexBp.System'))
            else:
                ReqRunLog(name+"\t"+"LoginCtl"+"\t密码输入错误")
                flash("密码输入错误.")
        else:
            ReqRunLog(session["online"]+"\t"+"LoginCtl"+"\t账户不存在")
            flash("账户不存在.")
    if form.errors:
        flash(form.errors)

    return render_template('login.html',form=form) 

@indexBp.route('/RegisterCtl',methods=['GET','POST'])
def RegisterCtl():
    '''注册表单验证'''
    form = RegisterForm(request.form)
    name = form.data["username"]
    if request.method == 'POST' and form.validate_on_submit():
        if form.data["code"] == g_codeLock:
            adminCtl = Admin()
            name = form.data["username"]
            if name in adminCtl.dicAdmin.keys():
                ReqRunLog(name+"\t"+"RegisterCtl"+"\t用户名已存在")
                flash("用户名已存在.")
                return render_template('register.html',form=form) 

            #login_user(curr_user)#记录登录用户
            session["online"] = name
            #用户写入mysql数据库
            adminCtl = Admin()
            user_new = User() 
            user_new.id = len(adminCtl.dicAdmin)
            user_new.name = form.username.data
            user_new.permission = 2
            user_new.passwd = form.password.data
            user_new.set_password(form.password.data)
            #try:
            db.session.add(user_new)
            db.session.commit()

            return redirect(url_for('IndexBp.System'))
        else:
            ReqRunLog(name+"\t"+"RegisterCtl"+"\t邀请码错误,你不是有缘人")
            flash("邀请码错误,你不是有缘人.")
    if form.errors:
        flash(form.errors)
    return render_template('register.html',form=form) 



@indexBp.route('/Form_NotePad',methods=['GET','POST'])
def Form_NotePad():
    '''保存笔记到mysql'''
    ReqRunLog("Form_NotePad")
    note = request.form['note']
    #print(note)
    return ""

@indexBp.route('/error',methods=['GET','POST'])
def error():
    '''错误提示'''
    ReqRunLog("error")
    return render_template(
        'error.html'
        )

@indexBp.route('/GetPage/<nid>',methods=['GET','POST'])
def GetPage(nid):
    '''请求页面'''
    ReqRunLog("GetPage"+str(nid))
    return url_for("IndexBp.GetPageNum",nid=nid)
@indexBp.route('/GetPageNum/<nid>',methods=['GET','POST'])
def GetPageNum(nid):
    '''获取该num页面'''
    workDir,privateDir = GetWorkRoot()
    #print("请求页面")

    #path = os.path.abspath(__file__)
    g_numList = []#postmessage页面num
    for root,dirs,files in os.walk(workDir):
        for file in files:
            strSplit = file.split('.')
            #print(strSplit[0])
            g_numList.append(int(strSplit[0]))
    if int(nid) in g_numList:
        name = ""
        if "online" in session and  session["online"] != "":
            name = g_lastPrivate.GetNameById(str(nid))
        else:
            #print("未登录",name)
            name = g_lastUpload.GetNameById(str(nid))
        #print(privateDir + '/'+str(nid)+'.'+name+'.html')
        return render_template(privateDir + '/'+str(nid)+'.'+name+'.html')
    else:
        return render_template('error.html')


@indexBp.route("/GetUploadMsg",methods=["GET","POST"])
def GetUploadMsg():
    '''最新上传消息'''
    #print("GetUploadMsg请求消息")
    workDir,privateDir = GetWorkRoot()
    if "online" in session and  session["online"] != "":
        ReqRunLog(session["online"]+"\t"+"GetUploadMsg")
        #print(workDir)
        #print("登录")
        g_lastPrivate.SetForder(workDir)
        g_lastPrivate.WorkThread()
        lastFiles,uploadTime = g_lastPrivate.GetLastFiles()
    else:
        ReqRunLog("GetUploadMsg")
        print("未登录")
        g_lastUpload.SetForder(workDir)
        g_lastUpload.WorkThread()
        lastFiles,uploadTime = g_lastUpload.GetLastFiles()
    return simplejson.dumps({
        "LastUpload":lastFiles,
        "UploadTime":uploadTime,
        "UploadPath":privateDir,
        "UploadAdmin":"Root超级用户",
        "UploadBooks":"《周易》、《资本论》",
        "HistorySize":g_lastUpload.GetHisSize()
    })

@indexBp.route("/SearchArticle",methods=["GET","POST"])
def SearchArticle():
    '''文章查找'''
    data = request.get_data()
    searchRecv = simplejson.loads(data)

    result={"null":"false"}
    searchTxt = searchRecv["title"]

    ReqRunLog("SearchArticle"+"\t"+searchTxt)
    if 0 == len(searchTxt):
        return simplejson.dumps({"null":"true"})

    #print("查找内容：[%s]"%searchTxt)
    for index,name in g_lastUpload.mapFile.items():
        if searchTxt in name:
            result[name] = index
    if 1 != len(result):
        return result
    else:
        return simplejson.dumps({"null":"true"})

g_lastTime = 0#上一次写入时间
g_currDate = ""#当天日期
g_currCount = 0#当天写入次数
@indexBp.route("/EditCodeSave",methods=["GET","POST"])
def EditCodeSave():
    '''代码编辑器保存'''
    global g_lastTime 
    global g_currDate 
    global g_currCount

    workDir,privateDir = GetWorkRoot()
    data = request.get_data()
    editRecv = simplejson.loads(data)
    print("保存数据",editRecv)
    path = workDir + "\\..\\editCodeFile\\" + editRecv["FileName"]
    #print(path)
  
    currTime = datetime.now()  
    distance = abs(g_lastTime-currTime.second) 
    if distance < 2:
        ReqRunLog("EditCodeSave"+"\t"+path+"\t写入太频繁")
    g_lastTime = currTime.second

    currDay = time.strftime("%Y%m%d",time.localtime())
    if g_currDate != currDay:
        g_currDate = currDay
        g_currCount = 0

    if g_currCount > 500:
        ReqRunLog("EditCodeSave"+"\t"+path+"\t突破当天写入次数")
        return "突破当天写入次数"
    g_currCount += 1

    with open(path,"w",encoding='utf-8',errors="ignore")as fp:
        fp.writelines(editRecv["Content"])
    ReqRunLog("EditCodeSave"+"\t"+path+"\tsuccessful")
    return "successful"


def IterEditFile(path,listFiles):
    for root,dirs,files in os.walk(path):
        if files:
            for file in files:
                listFiles.append(file)
        if dirs:
            for dir in dirs:
                IterEditFile(forder + '/' +dir,listFiles)

@indexBp.route("/GetEditFile",methods=["GET","POST"])
def GetEditFile():
    '''获取保存的代码文件'''
    workDir,privateDir = GetWorkRoot()
    path = workDir + "\\..\\editCodeFile\\"

    listFiles = []
    IterEditFile(path,listFiles)

    #print("请求文件：",listFiles)
    ReqRunLog("GetEditFile"+"\t"+path)
    return simplejson.dumps({"EdiitFile":listFiles})

@indexBp.route("/EditCodeOpen",methods=["GET","POST"])
def EditCodeOpen():
    '''代开代码文件'''
    file = request.get_data()
    workDir,privateDir = GetWorkRoot()
    path = workDir + "\\..\\editCodeFile\\" + str(file,encoding='utf-8')

    if not os.path.exists(path):
        ReqRunLog("EditCodeOpen"+"\t"+path+"\t请求不存在目录文件")
        return simplejson.dumps({"code":[]})

    listLines = []
    with open(path,"r",encoding='utf-8',errors="ignore")as fp:
        listLines = fp.readlines()
    #print(listLines)
    ReqRunLog("EditCodeOpen"+"\t"+path)
    return simplejson.dumps({"code":listLines})

@indexBp.route("/EditCodeRename",methods=["GET","POST"])
def EditCodeRename():
    '''重命名文件'''
    workDir,privateDir = GetWorkRoot()
    data = request.get_data()
    editRecv = simplejson.loads(data)
    print("保存数据",editRecv)
    path = workDir + "\\..\\editCodeFile\\" + editRecv["FileName"]
    newPath = workDir + "\\..\\editCodeFile\\" + editRecv["NewFileName"]
    #print(path)
    os.rename(path,newPath)
    ReqRunLog("EditCodeRename"+"\t"+path+"\t"+editRecv["NewFileName"]+"\tsuccessful")
    return "successful"


if __name__ == "__main__":
    GetWorkRoot();