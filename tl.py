# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session, url_for, redirect, jsonify
from bookinfo import getBookAmount, getBookInfo, getBookList, savebookinfo, delbook
from borrowinfo import getBorrowInfo, saveborrowinf, backbooks, bookobjectsub
from userauth import uauth, changepasswd
from flask_sqlalchemy import SQLAlchemy
import flask_excel
import pyexcel_xls
import pyexcel_xlsx
from getbookpic import getbookpic

import demjson
import sys
import base64

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hb@chinatowe'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:!q2w3e4r@120.25.202.59/towerlib"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'bookinfo'

    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(200))
    isbn = db.Column(db.String(50))
    bookwriter = db.Column(db.String(50))
    booksend = db.Column(db.String(50))
    bookkind = db.Column(db.String(50))
    booknumber = db.Column(db.Integer)
    bookamount = db.Column(db.Integer)
    area = db.Column(db.String(50))

    def __init__(self, bookname, isbn, bookwriter, booksend, bookkind, booknumber, bookamount, area):
        self.bookname = bookname
        self.isbn = isbn
        self.bookwriter = bookwriter
        self.booksend = booksend
        self.bookkind = bookkind
        self.booknumber = booknumber
        self.bookamount = bookamount
        self.area = area

    def to_json(self):
        return {
            'bookname': self.bookname,
            'isbn': self.isbn,
            'bookwriter': self.bookwriter,
            'booksend': self.booksend,
            'bookkind': self.bookkind,
            'booknumber': self.booknumber,
            'bookamount': self.bookamount,
            'area': self.area
        }


@app.route("/hblib/inputbook", methods=['POST', 'GET'])
def inputbook():
    if request.method == 'POST':
        try:
            count = 0
            jsondata = request.values.to_dict()

            for datas in jsondata:
                for data in demjson.decode(datas)['result']:
                    if data[1] != 'isbn':
                        booksave = Book(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                        db.session.add(booksave)
                        count = count + 1

            db.session.commit()
            return demjson.encode({'result': count})
        except:
            return demjson.encode({'result': 0})


@app.route("/hblib/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify({"result": request.get_array(field_name='file')})
    else:
        return {"result": 'Error'}


# 网站首页
@app.route('/hblib/')
def index():
    return render_template('index.html')


# 借书首页
@app.route('/hblib/<areacode>')
def borrow(areacode):
    return render_template('borrow.html', areacode=areacode)


# 登录
@app.route('/hblib/login/', methods=['GET', 'POST'])
def login():
    if len(session.keys()) > 0:
        areaname = session['areaname']
        return render_template('return.html', areaname=areaname)
    else:
        return render_template('login.html')


# 修改密码
@app.route('/hblib/changepasswd', methods=['GET', 'POST'])
def changepass():
    if request.method == 'POST':
        username = str(request.values.get('username', 0)).strip()
        oldpasswd = str(request.values.get('oldpasswd', 0)).strip()
        newpasswd = str(request.values.get('newpasswd', 0)).strip()

        res = changepasswd(username, oldpasswd, newpasswd)

        return demjson.encode(res)


# 后台首页
@app.route('/hblib/render/', methods=['GET', 'POST'])
def render():
    if request.method == 'POST':

        username = request.form['username']
        password = base64.b64encode(base64.b64encode(request.form['password']))

        autres = uauth(username, password)

        if len(autres['result']) > 0 and len(autres['result'][0]['areaname']) > 0:
            session['areaname'] = autres['result'][0]['areaname']
            return render_template('return.html', areaname=session['areaname'])
        else:
            return render_template('login.html', result='用户名、密码错误，请重新输入！')

    else:
        if len(session.keys()) > 0:
            return render_template('return.html', areaname=session['areaname'])
        else:
            return redirect(url_for('login'))


# 书籍管理页面
@app.route('/hblib/bookinput')
def bookinput():
    if len(session.keys()) > 0:
        areaname = session['areaname']
        return render_template('inputbook.html', areaname=areaname)
    else:
        return render_template('login.html')


# 获得数目
@app.route('/hblib/getbooklist', methods=['GET', 'POST'])
def getblist():
    if request.method == 'GET':
        args = request.args.to_dict()
        keyt = str(args.get('keytype').encode('utf-8')).strip()
        keyw = str(args.get('keyword').encode('utf-8')).strip()
        areaname = str(args.get('areaname').encode('utf-8')).strip()

        bookamount = {'result': getBookList(keyt, keyw, areaname)}

    return demjson.encode(bookamount)


# 获得书籍剩余数量
@app.route('/hblib/getbamount', methods=['GET', 'POST'])
def getbamount():
    if request.method == 'GET':
        args = request.args.to_dict()
        keyt = str(args.get('keytype').encode('utf-8')).strip()
        keyw = str(args.get('keyword').encode('utf-8')).strip()

        bookamount = {'result': getBookAmount(keyt, keyw)}

    return demjson.encode(bookamount)


#
@app.route('/hblib/getbooks', methods=['GET', 'POST'])
def getbooks():
    if request.method == 'GET':
        args = request.args.to_dict()
        keyt = str(args.get('keytype').encode('utf-8')).strip()
        keyw = str(args.get('keyword').encode('utf-8')).strip()
        page = int(args.get('page').encode('utf-8'))

        bookarry = {'result': getBookInfo(keyt, keyw, page)}

    return demjson.encode(bookarry)


# 获取借阅信息
@app.route('/hblib/getborrowinfo', methods=['GET', 'POST'])
def getborrowinfos():
    if request.method == 'GET':
        args = request.args.to_dict()
        isbn = str(args.get('isbn').encode('utf-8')).strip()
        borrowuser = str(args.get('borrowuser').encode('utf-8')).strip()
        areaname = str(args.get('areaname').encode('utf-8')).strip()

        borrowarry = {'result': getBorrowInfo(isbn, borrowuser, areaname)}

    return demjson.encode(borrowarry)


# 记录借阅信息
@app.route('/hblib/saveborrowinfo', methods=['GET', 'POST'])
def saveborrowinfo():
    if request.method == 'GET':
        args = request.args.to_dict()
        isbn = str(args.get('isbn').encode('utf-8')).strip()
        borrowuser = str(args.get('borrowuser').encode('utf-8')).strip()
        borrowdate = str(args.get('borrowdate').encode('utf-8')).strip()
        bookname = str(args.get('bookname').encode('utf-8')).strip()
        areaname = str(args.get('areaname').encode('utf-8')).strip()

        savewarry = {'result': saveborrowinf(bookname, isbn, borrowuser, borrowdate, areaname)}

    return demjson.encode(savewarry)


# 还书
@app.route('/hblib/backbook', methods=['GET', 'POST'])
def backbook():
    if request.method == 'GET':
        args = request.args.to_dict()

        b_order = str(args.get('b_order').encode('utf-8')).strip()
        back_date = str(args.get('back_date').encode('utf-8')).strip()
        isbn = str(args.get('isbn').encode('utf-8')).strip()
        areaname = str(args.get('areaname').encode('utf-8')).strip()

        backarry = {'result': backbooks(b_order, back_date, isbn, areaname)}

    return demjson.encode(backarry)


# 发放实物标记
@app.route('/hblib/objectsubmit', methods=['GET', 'POST'])
def booksubmit():
    if request.method == 'GET':
        args = request.args.to_dict()

        b_order = str(args.get('b_order').encode('utf-8')).strip()

        booksubarry = {'result': bookobjectsub(b_order)}

    return demjson.encode(booksubarry)


# 新增书籍
@app.route('/hblib/savebook', methods=['GET', 'POST'])
def savebook():
    if request.method == 'GET':
        args = request.args.to_dict()

        bookname = str(args.get('bookname').encode('utf-8')).strip()
        bookisbn = str(args.get('bookisbn').encode('utf-8')).strip()
        bookwriter = str(args.get('bookwriter').encode('utf-8')).strip()
        booksend = str(args.get('booksend').encode('utf-8')).strip()
        bookkind = str(args.get('bookkind').encode('utf-8')).strip()
        booknumber = str(args.get('booknumber').encode('utf-8')).strip()

        savearry = {'result': savebookinfo(bookname, bookisbn, bookwriter, booksend, bookkind, booknumber)}

    return demjson.encode(savearry)


# 删除书籍
@app.route('/hblib/delbook', methods=['GET', 'POST'])
def dbook():
    if request.method == 'POST':
        count = 0
        datas = request.values.to_dict()
        idarry = str(datas['data']).split(',')

        for id in idarry:
            res = Book.query.get_or_404(id)
            db.session.delete(res)
            count = count + 1

        db.session.commit()

    return demjson.encode({'result': count})


# 下载图片
@app.route('/hblib/downpic', methods=['GET', 'POST'])
def downpic():
    if request.method == 'GET':
        args = request.args.to_dict()

        areaname = str(args.get('areaname').encode('utf-8')).strip()

        downres = jsonify({'result': getbookpic.getisbn(areaname)})

        return downres


if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
