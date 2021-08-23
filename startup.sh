# Update and install
apt-get update
apt-get install -yq git supervisor python python-pip
pip install --upgrade pip virtualenv

# Add user to run job
useradd -m -d /home/botrunner botrunner

# Fetch source code
export HOME=/root
git clone https://github.com/SethBorder/BottyG.git /bots/botty_g

# Set up venv
python3 -m venv /bots/botty_g/env
source /bots/botty_g/env/bin/activate
/bots/botty_g/env/bin/pip install -r /bots/botty_g/requirements.txt

# Set ownership to runner account
chown -R botrunner:botrunner /bots/botty_g

# Deploy supervisor configs
cp /bots/botty_g/python_app.conf /etc/supervisor/conf.d/python_app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
