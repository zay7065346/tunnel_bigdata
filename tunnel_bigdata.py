#encoding: utf-8

from flask import Flask, render_template, request, redirect,url_for,session,g
import config
from models import User,Article,Comment
from exts import db
from functools import wraps
from login_required import login_required
from sqlalchemy import or_



app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'articles': Article.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)


@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone)
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码错误，请确认后再登录'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #手机号码合法验证
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已经被注册了，请更换手机号码'
        else:
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写!'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，跳转到登录页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.route('/article/',methods = ['GET','POST'])
@login_required
def article():
    if request.method == 'GET':
        return render_template('article.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        article = Article(title = title, content = content)
        article.author = g.user
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<article_id>/')
def detail(article_id):
    article_model =  Article.query.filter(Article.id == article_id).first()
    return render_template('detail.html',article=article_model)

@app.route('/add_comment/',methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('comment_content')
    article_id = request.form.get('article_id')
    comment = Comment(content = content)
    comment.author = g.user
    article = Article.query.filter(Article.id == article_id).first()
    comment.article = article
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',article_id=article_id))

@app.route('/search')
def search():
    q = request.args.get('q')
    articles = Article.query.filter(or_(Article.title.contains(q),Article.content.contains(q))).order_by('-create_time')
    return render_template('index.html',articles = articles)

@app.route('/aboutus')
def about():
    return render_template('aboutus.html')


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
            return {'user':g.user}
    return {}



if __name__ == '__main__':
    app.run()



