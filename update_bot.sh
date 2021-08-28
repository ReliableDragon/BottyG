rm main.py
curl -o main.py https://raw.githubusercontent.com/SethBorder/BottyG/main/main.py
chown botrunner:botrunner main.py
supervisorctl restart all