# -*- coding: utf-8 -*-

import MySQLdb

def getBookAmount(keytype,keyword):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
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
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
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


def getBookList(keytype,keyword,areaname):
    bookarry = []
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()

        if len(keyword) > 0:
            sqlstr = "select * from bookinfo where {0} like '%{1}%' and area = '{2}'".format(keytype,keyword,areaname)
        else:
            sqlstr = "select * from bookinfo where area = '{0}'".format(areaname)



        cur.execute(sqlstr)

        results = cur.fetchall()

        for result in results:
            bookname = result[0]
            bookwriter = result[2]
            booksend = result[3]
            bookkind = result[4]
            bookamount = result[6]
            isbn = result[1]
            id = result[8]
            area = result[7]
            booknumber = result[5]


            binfo = {'bookname': bookname,
                     'bookwriter': bookwriter,
                     'booksend': booksend,
                     'bookkind': bookkind,
                     'bookamount': bookamount,
                     'isbn':isbn,
                     'id':id,
                     'area':area,
                     'booknumber':booknumber}

            bookarry.append(binfo)

        return sorted(bookarry, key=lambda x: x['id'] ,reverse=False)

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


def savebookinfo(bookname,bookisbn,bookwriter,booksend,bookkind,booknumber):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
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

def delbook(id):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()
        delsql = "delete from bookinfo where id = '{0}' ".format(id)

        cur.execute(delsql)
        conn.commit()

        return cur.rowcount

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    keytype = 'bookwriter'
    keyword = ''
    areaname = '恩施'

    bookname = '12'
    bookisbn = '1234'
    bookwriter = '22222'
    booksend = '1222'
    bookkind = '小说'
    booknumber = '1'

    # print savebookinfo(bookname,bookisbn,bookwriter,booksend,bookkind,booknumber)
    # print getBookAmount(keytype,keyword)

    # print getBookAmount(keytype, keyword)
    # print getBookList(keytype,keyword,areaname)

    print delbook(138)
