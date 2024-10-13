
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):
    """配置参数"""
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:Mabu_72638934@127.0.0.1:3306/db_web"

    # 设置sqlalchemy自动更新跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# 连接数据库
app.config.from_object(Config)

import pymysql
pymysql.install_as_MySQLdb()

# 创建数据库aqlalchemy工具对象
db = SQLAlchemy(app)

# 创建数据库模型类
class Role(db.Model):
    """用户角色/身份表"""
    __tablename__ = "tbl_roles"

    id = db.Column(db.Integer, primary_key=True)  # 整型的主键，会默认设置为自增主键
    name = db.Column(db.String(32), unique=True)
    users = db.relationship("User", backref="role")  # 当role.users调用时，指明调用的是User的模型类;brakrefk可以用于反推，当user.role时，将上层对象进行打印


# 创建数据库模型类
class User(db.Model):
    """用户表"""
    __tablename__ = "tbl_users"  # 指明数据库的表名

    id = db.Column(db.Integer, primary_key=True)  # 整型的主键，会默认设置为自增主键
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    passward = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))  # 使Role类和User类建立联系

@app.route("/")
def start():
    return "This is the beginning"

if __name__ == '__main__':
    #app.run(host="127.0.0.1", port=8000, debug=True)

    with app.app_context():

        # 清除数据库里的所有数据, 谨慎使用
        db.drop_all()

        # 创建所有的表
        db.create_all()

        # 创建对象
        role1 = Role(name="admin")
        # session记录对象任务
        db.session.add(role1)
        # 提交任务到数据库中
        db.session.commit()

        # 创建对象
        role2 = Role(name="stuff")
        # session记录对象任务
        db.session.add(role2)
        # 提交任务到数据库中
        db.session.commit()

        # 添加数据
        user_1 = User(name="zhangsan", email="123@123.com", passward="123", role_id=role1.id)
        user_2 = User(name="lisi", email="234@234.com", passward="234", role_id=role1.id)
        user_3 = User(name="wangwu", email="345@345.com", passward="345", role_id=role2.id)
        user_4 = User(name="zhaoliu", email="456@456.com", passward="456", role_id=role2.id)

        # 以列表的形式一次保存多条数据
        db.session.add_all([user_1, user_2, user_3, user_4])
        db.session.commit()
