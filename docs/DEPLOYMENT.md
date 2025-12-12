# Deployment Guide

Guide for deploying InvoiceGen Backend to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Application Deployment](#application-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Security Checklist](#security-checklist)
- [Monitoring](#monitoring)

---

## Prerequisites

- Python 3.14+
- PostgreSQL 12+
- Domain name (for production)
- SSL certificate
- Server with at least 1GB RAM

---

## Environment Setup

### 1. Production Environment Variables

Create `.env.production`:

```env
# Application
ENVIRONMENT=production
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@db-host:5432/invoicegen_prod

# JWT Configuration
JWT_SECRET=<generate-strong-random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security
SECRET_KEY=<generate-strong-random-secret>

# Email (if configured)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
```

### 2. Generate Secrets

```python
import secrets

# Generate JWT secret
print(secrets.token_urlsafe(32))

# Generate secret key
print(secrets.token_urlsafe(32))
```

---

## Database Setup

### 1. Create Production Database

```sql
CREATE DATABASE invoicegen_prod;
CREATE USER invoicegen_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE invoicegen_prod TO invoicegen_user;
```

### 2. Run Migrations

```bash
# Set environment
export DATABASE_URL=postgresql://user:password@host:5432/invoicegen_prod

# Run migrations
alembic upgrade head
```

### 3. Backup Strategy

Set up automated backups:

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U invoicegen_user invoicegen_prod > backup_$DATE.sql
gzip backup_$DATE.sql

# Keep only last 30 days
find /backups -name "backup_*.sql.gz" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup-script.sh
```

---

## Application Deployment

### Option 1: Systemd Service

1. **Create service file** `/etc/systemd/system/invoicegen.service`:

```ini
[Unit]
Description=InvoiceGen Backend API
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/invoicegen_backend
Environment="PATH=/var/www/invoicegen_backend/.venv/bin"
EnvironmentFile=/var/www/invoicegen_backend/.env.production
ExecStart=/var/www/invoicegen_backend/.venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. **Enable and start service**:

```bash
sudo systemctl daemon-reload
sudo systemctl enable invoicegen
sudo systemctl start invoicegen
sudo systemctl status invoicegen
```

### Option 2: Gunicorn

1. **Install Gunicorn**:

```bash
pip install gunicorn
```

2. **Create Gunicorn config** `gunicorn_config.py`:

```python
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
accesslog = "/var/log/invoicegen/access.log"
errorlog = "/var/log/invoicegen/error.log"
loglevel = "info"
```

3. **Run Gunicorn**:

```bash
gunicorn app.main:app -c gunicorn_config.py
```

### Option 3: Nginx Reverse Proxy

1. **Install Nginx**:

```bash
sudo apt install nginx
```

2. **Create Nginx config** `/etc/nginx/sites-available/invoicegen`:

```nginx
upstream invoicegen_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    access_log /var/log/nginx/invoicegen_access.log;
    error_log /var/log/nginx/invoicegen_error.log;

    # Max upload size
    client_max_body_size 10M;

    location / {
        proxy_pass http://invoicegen_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # GraphQL endpoint
    location /graphql {
        proxy_pass http://invoicegen_backend/graphql;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable site**:

```bash
sudo ln -s /etc/nginx/sites-available/invoicegen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

4. **SSL with Let's Encrypt**:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

---

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.14-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: invoicegen
      POSTGRES_USER: invoicegen
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U invoicegen"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://invoicegen:${DB_PASSWORD}@db:5432/invoicegen
      JWT_SECRET: ${JWT_SECRET}
      ENVIRONMENT: production
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

### 3. Build and Run

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

---

## Cloud Platforms

### AWS Elastic Beanstalk

1. **Install EB CLI**:

```bash
pip install awsebcli
```

2. **Initialize**:

```bash
eb init -p python-3.14 invoicegen-backend
```

3. **Create environment**:

```bash
eb create invoicegen-prod
```

4. **Deploy**:

```bash
eb deploy
```

### Heroku

1. **Create Procfile**:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
release: alembic upgrade head
```

2. **Deploy**:

```bash
heroku create invoicegen-backend
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### DigitalOcean App Platform

1. **Create app.yaml**:

```yaml
name: invoicegen-backend
services:
  - name: api
    github:
      repo: your-username/invoicegen-backend
      branch: main
    build_command: pip install -r requirements.txt
    run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
      - key: JWT_SECRET
        scope: RUN_TIME
        type: SECRET
    http_port: 8080

databases:
  - name: db
    engine: PG
    version: "15"
```

2. **Deploy**:

```bash
doctl apps create --spec app.yaml
```

---

## Security Checklist

- [ ] Use HTTPS/TLS for all connections
- [ ] Set strong JWT secret (32+ characters)
- [ ] Enable CORS only for trusted domains
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Enable database connection pooling
- [ ] Set up firewall rules
- [ ] Use strong database passwords
- [ ] Enable database SSL connections
- [ ] Implement request logging
- [ ] Set up intrusion detection
- [ ] Regular security updates
- [ ] Implement backup strategy
- [ ] Use non-root user for application
- [ ] Disable debug mode in production
- [ ] Implement API versioning
- [ ] Set up monitoring and alerts
- [ ] Regular penetration testing
- [ ] Implement input validation
- [ ] Use prepared statements (SQLAlchemy does this)

---

## Monitoring

### Application Monitoring

1. **Install Sentry**:

```bash
pip install sentry-sdk
```

2. **Configure in `app/main.py`**:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
    environment="production"
)
```

### Logging

Configure structured logging:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'logs/app.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
```

### Health Checks

Implement health check endpoint:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

### Metrics

Use Prometheus for metrics:

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## Troubleshooting

### Application won't start

1. Check logs: `journalctl -u invoicegen -n 50`
2. Verify environment variables
3. Test database connection
4. Check port availability

### Database connection errors

1. Verify DATABASE_URL
2. Check PostgreSQL is running
3. Verify firewall rules
4. Test connection: `psql $DATABASE_URL`

### High memory usage

1. Reduce worker count
2. Implement connection pooling
3. Add caching layer (Redis)
4. Optimize database queries

### Slow response times

1. Add database indexes
2. Implement caching
3. Use CDN for static files
4. Optimize queries with EXPLAIN
5. Add load balancer

---

## Maintenance

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
alembic upgrade head

# Restart service
sudo systemctl restart invoicegen
```

### Database Maintenance

```sql
-- Vacuum database
VACUUM ANALYZE;

-- Reindex
REINDEX DATABASE invoicegen_prod;

-- Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## Support

For deployment issues:
- Documentation: [repository-url]/docs
- Issues: [repository-url]/issues
- Email: devops@invoicegen.com
