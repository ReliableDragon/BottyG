rm botty_g.py botty_g.py~
curl -o botty_g.py https://raw.githubusercontent.com/SethBorder/BottyG/main/botty_g.py
chown botrunner:botrunner botty_g.py
supervisorctl restart all