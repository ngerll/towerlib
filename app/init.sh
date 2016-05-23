sudo service nginx start
ntpdate -u cn.ntp.org.cn
gunicorn -w3 -b127.0.0.1:5000 tl:app