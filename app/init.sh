sudo service nginx start
ntpdate -u 210.72.145.44
gunicorn -w3 -b127.0.0.1:5000 tl:app