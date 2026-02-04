# 🚀 Deployment Guide

Panduan lengkap untuk deploy Support Ticket System ke berbagai platform.

## 📋 Table of Contents

- [Streamlit Cloud (Recommended)](#streamlit-cloud)
- [Heroku](#heroku)
- [Railway](#railway)
- [Docker](#docker)
- [VPS / Traditional Server](#vps)

---

## 🎈 Streamlit Cloud

**Pros:** Gratis, mudah, integrated dengan GitHub, auto-deploy

**Steps:**

### 1. Persiapan Repository

```bash
# Push ke GitHub
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Deploy

1. Kunjungi [share.streamlit.io](https://share.streamlit.io)
2. Login dengan GitHub account
3. Klik "New app"
4. Pilih repository Anda
5. Set main file: `support_ticket_system.py`
6. Klik "Deploy"

### 3. Configuration (Optional)

Buat file `.streamlit/config.toml` untuk customization:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
```

**Done!** Aplikasi akan tersedia di: `https://yourapp.streamlit.app`

---

## 🟣 Heroku

**Pros:** Mature platform, good for production, auto-deploy

### 1. Install Heroku CLI

```bash
# Download dari https://devcenter.heroku.com/articles/heroku-cli
# Atau via npm
npm install -g heroku
```

### 2. Buat File Konfigurasi

**Procfile:**
```
web: sh setup.sh && streamlit run support_ticket_system.py
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

**runtime.txt:**
```
python-3.11.0
```

### 3. Deploy

```bash
# Login ke Heroku
heroku login

# Create app
heroku create your-ticket-system

# Deploy
git push heroku main

# Open app
heroku open
```

### 4. Monitoring

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps
```

---

## 🚂 Railway

**Pros:** Modern, simple, generous free tier

### 1. Deploy via GitHub

1. Kunjungi [railway.app](https://railway.app)
2. Login dengan GitHub
3. Klik "New Project" → "Deploy from GitHub repo"
4. Pilih repository Anda
5. Railway akan auto-detect Streamlit app

### 2. Environment Variables (if needed)

```bash
# Via Railway dashboard
PYTHON_VERSION=3.11
```

### 3. Custom Domain (Optional)

1. Go to Settings
2. Add custom domain
3. Follow DNS configuration

---

## 🐳 Docker

**Pros:** Consistent environment, portable, scalable

### 1. Buat Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "support_ticket_system.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Buat .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
README.md
.DS_Store
```

### 3. Build & Run

```bash
# Build image
docker build -t ticket-system .

# Run container
docker run -p 8501:8501 ticket-system

# Run dengan volume (persistent data)
docker run -p 8501:8501 -v $(pwd)/data:/app/data ticket-system
```

### 4. Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  ticket-system:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

---

## 🖥️ VPS / Traditional Server

**Pros:** Full control, custom domain, production-ready

### 1. Server Requirements

- Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- Python 3.8+
- Nginx (recommended)
- 1GB RAM minimum

### 2. Initial Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install nginx (optional, for reverse proxy)
sudo apt install nginx -y
```

### 3. Deploy Application

```bash
# Clone repository
git clone https://github.com/yourusername/support-ticket-system.git
cd support-ticket-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test run
streamlit run support_ticket_system.py
```

### 4. Setup Systemd Service

**Create service file:** `/etc/systemd/system/ticket-system.service`

```ini
[Unit]
Description=Support Ticket System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/support-ticket-system
Environment="PATH=/path/to/support-ticket-system/venv/bin"
ExecStart=/path/to/support-ticket-system/venv/bin/streamlit run support_ticket_system.py --server.port 8501

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable ticket-system
sudo systemctl start ticket-system
sudo systemctl status ticket-system
```

### 5. Setup Nginx Reverse Proxy

**Create nginx config:** `/etc/nginx/sites-available/ticket-system`

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/ticket-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Setup SSL (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

---

## 🔧 Environment Variables

Untuk production, gunakan environment variables untuk konfigurasi sensitif:

**.env file:**
```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

**Load dalam aplikasi:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

port = os.getenv('STREAMLIT_SERVER_PORT', 8501)
```

---

## 📊 Monitoring & Logging

### Streamlit Cloud
- Built-in logs di dashboard
- App metrics tersedia

### Heroku
```bash
heroku logs --tail
heroku ps
```

### VPS
```bash
# View systemd logs
sudo journalctl -u ticket-system -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🔒 Security Checklist

- [ ] Update dependencies regularly
- [ ] Use HTTPS/SSL
- [ ] Set proper file permissions
- [ ] Enable firewall
- [ ] Regular backups
- [ ] Monitor logs
- [ ] Rate limiting (nginx)
- [ ] Input validation
- [ ] Secure data storage

---

## 🆘 Troubleshooting

### App tidak mau start

```bash
# Check logs
streamlit run support_ticket_system.py --logger.level=debug

# Check dependencies
pip install -r requirements.txt --upgrade
```

### Port sudah digunakan

```bash
# Kill process on port 8501
sudo lsof -ti:8501 | xargs kill -9

# Atau gunakan port lain
streamlit run support_ticket_system.py --server.port 8502
```

### Permission denied

```bash
# Fix permissions
chmod +x support_ticket_system.py
chown -R www-data:www-data /path/to/app
```

---

## 📞 Support

Jika ada masalah saat deployment:

- Check [Streamlit Docs](https://docs.streamlit.io/deploy)
- Open issue di GitHub
- Email: your.email@example.com

---

**Happy Deploying! 🚀**