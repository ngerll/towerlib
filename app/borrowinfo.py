# -*- coding: utf-8 -*-

import MySQLdb

def getBorrowInfo(isbn, borrowuser,areaname): #获取借阅记录
    try:
        binfoarr = []

        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()

        if len(isbn) > 0:
            sqlstr = "select * from borrow_record where isbn = '{0}' and b_user = '{1}' and back_date is null and area = '{2}' ".format(isbn, borrowuser,areaname)
        elif len(borrowuser) > 0 :
            sqlstr = "select * from borrow_record where b_user = '{0}' and back_date is null and area = '{1}' ".format(borrowuser,areaname)
        else:
            sqlstr = "select * from borrow_record where back_date is null and area = '{0}' ".format(areaname)

        cur.execute(sqlstr)

        rcout = cur.rowcount
        if rcout > 0:
            results = cur.fetchall()

            for result in results:
                b_order = int(result[0])
                bookname = result[1]
                isbn = result[2]
                borrowdate = result[4]
                object_out = result[7]
                area = result[8]
                b_user = result[3]

                binfo = {'b_order':b_order,
                         'bookname':bookname,
                         'isbn':isbn,
                         'borrowdate':borrowdate,
                         'object_out':object_out,
                         'areaname':area,
                         'b_user': b_user}

                binfoarr.append(binfo)

        return sorted(binfoarr, key=lambda x: x['borrowdate'] ,reverse=False)

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


def saveborrowinf(bookname, isbn, borrowuser, borrowdate,areaname):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()
        insertsql = "insert into borrow_record (bookname,isbn,b_user,borrow_date,area) values ('{0}','{1}','{2}','{3}','{4}')" .format(bookname, isbn, borrowuser, borrowdate,areaname)

        cur.execute(insertsql)
        conn.commit()

        reduceBook(isbn, areaname) #减少库存

        return cur.rowcount

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


def backbooks(b_order, back_date, isbn,areaname):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()
        updatesql = "update borrow_record set back_date = '{0}' where b_order = '{1}'" .format(back_date, b_order)

        cur.execute(updatesql)
        conn.commit()

        addBook(isbn, areaname) #增加库存

        return cur.rowcount

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()



def addBook(isbn, areaname):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()
        amountsql = "select bookamount from bookinfo where isbn = '{0}' and area = '{1}' ".format(isbn, areaname)

        cur.execute(amountsql)
        amount = int(cur.fetchall()[0][0]) + 1

        sqlstr = "update bookinfo set bookamount = {0} where isbn = '{1}' and area = '{2}' ".format(amount, isbn, areaname)
        cur.execute(sqlstr)
        conn.commit()
        return cur.rowcount

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()

def reduceBook(isbn,areaname):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()
        amountsql = "select bookamount from bookinfo where isbn = '{0}' and area = '{1}' ".format(isbn, areaname)

        cur.execute(amountsql)
        amount = int(cur.fetchall()[0][0])
        if amount > 0:
            amount = amount - 1
            sqlstr = "update bookinfo set bookamount = {0} where isbn = '{1}' and area = '{2}' ".format(amount,isbn,areaname)
            cur.execute(sqlstr)
            conn.commit()
            return cur.rowcount
        else:
            return 0

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()



def bookobjectsub(b_order):
    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()
        updatesql = "update borrow_record set object_out = '1' where b_order = '{0}'" .format(b_order)

        cur.execute(updatesql)
        conn.commit()

        return cur.rowcount

    except:
        return "Error"
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
   b_order = '2'
   isbn = '9787545908558'
   borrowuser = '秦立夏'
   bookname = '每个人的故乡都在沦陷'
   borrowdate = '2016-04-21 11:56:58'
   back_date = '2016-04-22 00:15:29'

   # print getBorrowInfo(isbn,borrowuser)
   # print addBook(isbn)

   # print saveborrowinf(bookname, isbn, borrowuser, borrowdate)

   print getBorrowInfo('','胡乔','省分')

