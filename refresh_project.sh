git fetch origin main
git reset --hard FETCH_HEAD
chown -R botrunner:botrunner /bots/botty_g

supervisorctl reread
supervisorctl update
supervisorctl restart all