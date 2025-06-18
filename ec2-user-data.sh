#!/bin/bash

# Update and install dependencies
apt-get update -y
apt-get install -y python3-pip python3-venv nginx git

# Clone your project (replace with your repo URL)
cd /home/ubuntu
git clone https://github.com/rahulkothuri/judiciobot-backend.git
cd judicobot-backend

# Set up virtual environment and install requirements
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create Gunicorn start script
cat <<EOF > gunicorn_start.sh
#!/bin/bash
source venv/bin/activate
exec gunicorn -k uvicorn.workers.UvicornWorker fastapp:app --bind 0.0.0.0:8000
EOF
chmod +x gunicorn_start.sh

# Create NGINX config
cat <<EOF > nginx_judiciobot.conf
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Configure NGINX
mv nginx_judiciobot.conf /etc/nginx/sites-available/judiciobot
ln -s /etc/nginx/sites-available/judiciobot /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
systemctl restart nginx

# Start the FastAPI app with Gunicorn (background)
./gunicorn_start.sh &
