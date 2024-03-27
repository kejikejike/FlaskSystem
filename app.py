# 导入Flask 模板
from flask import Flask,render_template,request,redirect
# 导入要用到的数据库 第三方库
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 连接数据库的配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/DetectSystem?charset=utf8mb4'
db = SQLAlchemy(app)

# 创建好用户信息的表格的信息
class User(db.Model):
    __tablename__ = "DetectSystem_user"
    id = db.Column(db.Integer, primary_key=True,comment="用户id")
    password = db.Column(db.String(20), nullable=False,comment="用户密码")


# 执行所有的创建表格的语句
with app.app_context():
    db.create_all()

#登录的路由
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        id = request.form.get('name')
        pwd = request.form.get('password')
        a = User.query.filter_by(id=int(id)).first()
        if a.password == pwd and int(id) == a.id:
            return redirect('index')
    return render_template('login.html')

#注册的路由
@app.route('/res', methods=["GET", "POST"])
def res():
    if request.method == 'POST':
        id = request.form.get('name')
        passwd = request.form.get('password')
        pwd_q = request.form.get('password_to')
        a = User.query.filter_by(id=id).first()
        b = User.query.filter_by(id=id).all()
        print(a)
        # print(a.name)
        if pwd_q != passwd:
            return '密码不一致！请返回重新输入！'

        if a is None:
            user = User(id=int(id), password=passwd)
            db.session.add(user)
            db.session.commit()
            return redirect('login')
        if int(id) == a.id:
            return '已存在该用户！'
    return render_template('res.html')

#登录成功后返回index
@app.route('/index')
def admin():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
