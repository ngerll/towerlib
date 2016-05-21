# -*- coding: utf-8 -*-

import requests
import re
import MySQLdb
import os


def getisbn(areaname):
    conn = MySQLdb.connect(host='120.25.202.59', user='root', passwd='!q2w3e4r', db='towerlib', port=3306,
                           charset='utf8')
    cur = conn.cursor()

    sqlstr = "select * from bookinfo where area = '{0}'".format(areaname)

    cur.execute(sqlstr)

    results = cur.fetchall()

    count = 0

    for result in results:
        isbn = str(result[1])
        if len(isbn) == 13:
            number = getbookpic(isbn, isbn)
        else:
            isbnnew = isbn[0:13]
            number = getbookpic(isbnnew, isbn)

        count = number + count

    cur.close()
    conn.close()

    return count


def getbookpic(isbn, picname):
    url = 'http://search.jd.com/Search'

    params = {'keyword': isbn,
              'enc': 'utf-8',
              'wq': isbn}

    respone = requests.get(url, params=params).text

    result = re.findall('class="err-product" data-img="1" src="//(.*?)" />', respone, re.S)

    count = 0

    filename = "/var/www/app/static/bookpic/" + picname + '.jpg'

    if len(result) > 0:
        if os.path.exists(filename):
            pass
        else:
            savebookpic(result[0], filename)
            count = count + 1

    return count


def savebookpic(url, filename):
    url = 'http://' + url

    respone = requests.get(url).content

    with open(filename, 'wb') as file:
        file.write(respone)


if __name__ == '__main__':
    # isbn = '9787535461940'
    # getbookpic(isbn)
    print getisbn('黄石')
