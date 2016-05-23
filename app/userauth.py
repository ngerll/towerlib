# -*- coding: utf-8 -*-

import MySQLdb
import base64

def uauth(username, passwd): #登录验证
    uautharr = []

    try:
        conn = MySQLdb.connect(host='220.249.117.234',user='root',passwd='!q2w3e4r',db='towerlib',port=9001,charset='utf8')
        cur = conn.cursor()

        password = base64.b64decode(base64.b64decode(passwd))

        uauthsql = "select * from adminuser where userid = '{0}' and passwd = '{1}' ".format(username,password)
        cur.execute(uauthsql)

        rcount = cur.rowcount
        if rcount > 0:
            results = cur.fetchall()

            for result in results:
                areaname = result[2]

                uauthinfo = {'areaname':areaname}

                uautharr.append(uauthinfo)

        return {'result':uautharr}

    except:
        return {'result':'Error'}
    finally:
        cur.close()
        conn.close()


def changepasswd(username, oldpasswd,newpasswd): #修改密码

    try:
        conn = MySQLdb.connect(host='220.249.117.234', user='root', passwd='!q2w3e4r', db='towerlib', port=9001,
                               charset='utf8')
        cur = conn.cursor()


        uauthsql = "update adminuser set passwd = '{0}' where userid = '{1}' and passwd = '{2}' ".format(newpasswd, username, oldpasswd)
        cur.execute(uauthsql)


        rcount = cur.rowcount

        if rcount > 0:
            conn.commit()
            return {'result': rcount}
        else:
            return {'result':0}


    except:
        return {'result':'Error'}
    finally:
        cur.close()
        conn.close()


def getarealist(): #登录验证
    areaarr = []

    try:
        conn = MySQLdb.connect(host='220.249.117.234',user='root',passwd='!q2w3e4r',db='towerlib',port=9001,charset='utf8')
        cur = conn.cursor()


        areaqry = "select * from adminuser"
        cur.execute(areaqry)

        rcount = cur.rowcount
        if rcount > 0:
            results = cur.fetchall()

            for result in results:
                areacode = result[0]
                areaname = result[2]

                arealist = {'areaname':areaname,
                            'areacode':areacode}

                areaarr.append(arealist)

        return areaarr

    except:
        return 'Error'
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    username = 'hubei'
    newpasswd = '222222'
    oldpasswd = '123456'

    # print uauth(username,passwd)['result'][0]['areaname']
    # print changepasswd(username,oldpasswd,newpasswd)
    print getarealist()