# Add user to run job
useradd -m -d /home/botrunner botrunner

mkdir /bots/botty_g

# Set ownership to runner account
chown -R botrunner:botrunner /bots/botty_g

# Update and install
apt-get update
apt-get install -yq git supervisor python python-pip
pip install --upgrade pip virtualenv
pip install --upgrade firebase-admin

# Fetch source code
export HOME=/root
git clone https://github.com/SethBorder/BottyG.git /bots/botty_g

# Set up venv
virtualenv -p python3 /bots/botty_g/env
source /bots/botty_g/env/bin/activate
/bots/botty_g/env/bin/pip install -r /bots/botty_g/requirements.txt

# Deploy supervisor configs
cp /bots/botty_g/python_app.conf /etc/supervisor/conf.d/python_app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
supervisorctl restart all