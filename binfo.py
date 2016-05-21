# -*- coding: utf-8 -*-

import MySQLdb



urlhost = MySQLdb.connect(host='120.25.202.59',user='root',passwd='!q2w3e4r',db='towerlib',port=3306,charset='utf8')


def getBookAmount(keytype,keyword):
    try:
        conn = urlhost
        cur = conn.cursor()
        if len(keyword) > 0:
            sqlstr = "select * from bookinfo where {0} like '%{1}%' ".format(keytype,keyword)
        else:
            sqlstr = "select * from bookinfo"


        cur.execute(sqlstr)
        pagecount = cur.rowcount

        return pagecount
    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


def getBookInfo(keytype,keyword,page):
    bookarry = []
    try:
        conn = urlhost
        cur = conn.cursor()

        start = (page-1)*10
        end = 10

        if len(keyword) > 0:
            sqlstr = "select * from bookinfo where {0} like '%{1}%' limit {2},{3}".format(keytype,keyword,start,end)
        else:
            sqlstr = "select * from bookinfo limit %d,%d" % (start, end)

        cur.execute(sqlstr)

        results = cur.fetchall()

        for result in results:
            bookname = result[0]
            bookwriter = result[2]
            booksend = result[3]
            bookkind = result[4]
            bookamount = result[6]
            isbn = result[1]

            binfo = {'bookname': bookname,
                     'bookwriter': bookwriter,
                     'booksend': booksend,
                     'bookkind': bookkind,
                     'bookamount': bookamount,
                     'isbn':isbn}

            bookarry.append(binfo)

        return bookarry

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


def getBookList(keytype,keyword):
    bookarry = []
    try:
        conn = urlhost
        cur = conn.cursor()

        if len(keyword) > 0:
            sqlstr = "select * from bookinfo where {0} like '%{1}%'".format(keytype,keyword)
        else:
            sqlstr = "select * from bookinfo"

        cur.execute(sqlstr)

        results = cur.fetchall()

        for result in results:
            bookname = result[0]
            bookwriter = result[2]
            booksend = result[3]
            bookkind = result[4]
            bookamount = result[6]
            isbn = result[1]

            binfo = {'bookname': bookname,
                     'bookwriter': bookwriter,
                     'booksend': booksend,
                     'bookkind': bookkind,
                     'bookamount': bookamount,
                     'isbn':isbn}

            bookarry.append(binfo)

        return bookarry

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


def savebookinfo(bookname,bookisbn,bookwriter,booksend,bookkind,booknumber):
    try:
        conn = urlhost
        cur = conn.cursor()

        savesql = "insert into bookinfo values ('{0}','{1}','{2}','{3}','{4}',{5},{6})".format(bookname,bookisbn,bookwriter,booksend,bookkind,int(booknumber),int(booknumber))

        cur.execute(savesql)
        conn.commit()

        return cur.rowcount

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    keytype = 'bookwriter'
    keyword = '习'

    bookname = '12'
    bookisbn = '1234'
    bookwriter = '22222'
    booksend = '1222'
    bookkind = '小说'
    booknumber = '1'

    # print DB.savebookinfo(bookname,bookisbn,bookwriter,booksend,bookkind,booknumber)

    print getBookAmount(keytype,keyword)

    # print getBookAmount(keytype, keyword)
