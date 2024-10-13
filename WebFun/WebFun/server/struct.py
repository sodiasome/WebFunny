from . import app

import pymysql
from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)


from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
#   1.mysql数据表结构
class User(UserMixin,db.Model):
    '''
    用户表
    '''
    __tablename__ = 'tb_User'
    id = db.Column(db.Integer, primary_key=True,autoincrement=False)    # id
    name = db.Column(db.String(64), nullable=False)                     # 用户名
    passwd = db.Column(db.String(512), nullable=False)                  # 加密密码
    permission = db.Column(db.Integer, nullable=False)                  # 权限
    loginIp = db.Column(db.String(64))                                  # 用户登录ip
    registerTime = db.Column(db.String(64))                             # 注册时间
    sumTime = db.Column(db.Integer)                                  # 在线时长 小时
    lastTime = db.Column(db.String(64))                                 # 上次登录时间

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self,passwd, password):
        return check_password_hash(passwd, password)

class Note(UserMixin,db.Model):
    '''
    留言墙
    '''
    __tablename__ = 'tb_Note'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)#用户
    noteTime = db.Column(db.String(64), nullable=False)#留言时间
    noteTxt = db.Column(db.String(2048), nullable=False)#留言内容
    noteFlag = db.Column(db.String(64), nullable=False)#关键字

class Article(UserMixin,db.Model):
    '''
    文章表
    '''
    __tablename__ = 'tb_Article'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)#作者
    articleTime = db.Column(db.String(64), nullable=False)#发表时间
    articlePath = db.Column(db.String(512), nullable=False)#文章路径
    noteFlag = db.Column(db.String(64), nullable=False)#文章名

class Book(UserMixin,db.Model):
    '''
    书籍表
    '''
    __tablename__ = 'tb_Book'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)#上传用户
    bookTime = db.Column(db.String(64), nullable=False)#上传时间
    bookName = db.Column(db.String(64), nullable=False)#书名
    bookPath = db.Column(db.String(512), nullable=False)#上传路径

class People(UserMixin,db.Model):
    '''
    名人表
    '''
    __tablename__ = 'tb_People'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)#名字
    bornTime = db.Column(db.String(64), nullable=False)#出生时间
    deadTime = db.Column(db.String(64), nullable=True)#去世时间
    scription = db.Column(db.String(2048), nullable=False)#介绍

class Permission(UserMixin,db.Model):
    '''
    权限表
    '''
    __tablename__ = 'tb_Permission'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)#用户
    level = db.Column(db.Integer, nullable=False)#权限等级


def CreateTable():
    with app.app_context():
        db.drop_all()

        db.create_all()

        init_root = User()              # 插入超級用戶
        init_root.id = 0
        init_root.name="root"
        init_root.permission = 1

        passwd = "888#hans"
   
        init_root.passwd = generate_password_hash(passwd)#
        init_root.loginIp = "127.0.0.1"                      # 用户登录ip
        init_root.registerTime = "2022/03/17/13:31:00"       # 注册时间
        init_root.sumTime = 0                                # 在线时长
        init_root.lastTime = "2022/03/17/13:31:00"           # 上次登录时间

        try:
            db.session.add(init_root)
            db.session.commit()
            print("root已初始化")
        except Exception :
            print("root创建失败")

        #perm_list = ["超级用户","一级用户","二级用户"]  # 权限表格数据初始化
        #try:
        #    db.session.execute(
        #        Permission.__table__.insert(),
        #        [{"id":i+1,"name":"","level":perm_list[i]} for i in range(0,len(perm_list))]
        #        )
        #    db.session.commit()
        #    print("权限初始化成功")
        #except Exception as e:
        #    db.session.rollback()
        #    print("权限初始化失败")







from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email,EqualTo
#   2.FlaskForm
class RegisterForm(FlaskForm):
    code = PasswordField("邀请码：", validators=[DataRequired("请输入邀请码")],render_kw={"placeholder": "请输入邀请码"})
    username = StringField("用户：", validators=[DataRequired("请输入用户名")], render_kw={"placeholder": "请输入用户名"})
    password = PasswordField("密码：", validators=[DataRequired("请输入密码")],render_kw={"placeholder": "请输入密码"})
    password2 = PasswordField("确认密码：", validators=[DataRequired("请输入确认密码"), EqualTo("password", message="两次密码不一致")],render_kw={"placeholder": "请确认密码"})
    remember_me = BooleanField("记住我")
    submit = SubmitField("注册")

    def validate_passwd_repeat(self):
        if self.password != self.password2:
            return "两次密码不一致"
            
class LoginForm(FlaskForm):
    username = StringField("用户：", validators=[DataRequired("请输入用户名")], render_kw={"placeholder": "请输入用户名"})
    password = PasswordField("密码：", validators=[DataRequired("请输入密码")],render_kw={"placeholder": "请输入密码"})
    remember_me = BooleanField("记住我")


if __name__ == "__main__":


     db.create_all()



