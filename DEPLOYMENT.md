# Talk-Less Platform - Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start with Docker Compose](#quick-start-with-docker-compose)
3. [Production Deployment](#production-deployment)
4. [Configuration](#configuration)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Security Considerations](#security-considerations)

## Prerequisites

### Required
- Docker 20.10+ and Docker Compose 2.0+
- At least 2GB RAM
- At least 10GB disk space
- OpenAI API key OR Anthropic API key (for LLM summarization)

### Recommended
- 4GB+ RAM for production
- 50GB+ disk space for long-term storage
- SSL/TLS certificate for HTTPS
- Domain name

## Quick Start with Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/UnaverageDeveloper/Talk-Less.git
cd Talk-Less
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Required variables in `.env`:
```env
DB_PASSWORD=your_secure_password_here
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# Access API documentation
open http://localhost:8000/docs
```

## Production Deployment

### Architecture Overview

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────────────────────┐
│      Reverse Proxy (nginx)          │
│   HTTPS, Rate Limiting, Caching     │
└──────┬──────────────────────────────┘
       │
┌──────▼───────────┐    ┌──────────────┐
│   Talk-Less API  │───▶│    Redis     │
│   (FastAPI)      │    │   (Cache)    │
└──────┬───────────┘    └──────────────┘
       │
┌──────▼───────────┐    ┌──────────────┐
│ Pipeline Runner  │───▶│  PostgreSQL  │
│  (Scheduled)     │    │  (Storage)   │
└──────────────────┘    └──────────────┘
```

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Create application directory
sudo mkdir -p /opt/talkless
cd /opt/talkless
```

### Step 2: Configure Firewall

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Step 3: Set Up SSL/TLS (Recommended)

Using Let's Encrypt with Certbot:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --standalone -d your-domain.com

# Certificates will be at:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem
```

### Step 4: Configure nginx Reverse Proxy

Create `/etc/nginx/sites-available/talkless`:

```nginx
upstream talkless_api {
    server localhost:8000;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # CORS headers (Talk-Less is public API)
    add_header Access-Control-Allow-Origin "*" always;
    add_header Access-Control-Allow-Methods "GET, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Proxy to API
    location / {
        proxy_pass http://talkless_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Cache static responses
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        proxy_pass http://talkless_api;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/talkless /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: Deploy with Docker Compose

```bash
# Clone repository
cd /opt/talkless
git clone https://github.com/UnaverageDeveloper/Talk-Less.git .

# Configure environment
cp .env.example .env
nano .env  # Add your configuration

# Start services
docker-compose up -d

# Enable auto-restart
docker-compose restart
```

### Step 6: Set Up Automatic Updates

Create `/opt/talkless/update.sh`:

```bash
#!/bin/bash
# Talk-Less Auto-Update Script

cd /opt/talkless

# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Cleanup old images
docker image prune -f

echo "Update completed at $(date)"
```

Make executable and schedule:

```bash
chmod +x /opt/talkless/update.sh

# Add to crontab (weekly updates)
(crontab -l 2>/dev/null; echo "0 3 * * 0 /opt/talkless/update.sh >> /var/log/talkless-update.log 2>&1") | crontab -
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DB_PASSWORD` | Yes | - | PostgreSQL password |
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key for GPT-4 |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic API key for Claude |
| `LOG_LEVEL` | No | INFO | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `REDIS_URL` | No | redis://redis:6379/0 | Redis connection URL |
| `DATABASE_URL` | No | (auto-configured) | PostgreSQL connection URL |

*At least one LLM API key required

### Pipeline Configuration

Edit `backend/config/pipeline_config.yaml`:

```yaml
# How often to fetch articles (in minutes)
ingestion:
  fetch_interval: 30
  max_articles_per_source: 100

# Article grouping settings
comparison:
  min_articles_per_group: 2
  similarity_threshold: 0.7

# Summarization settings
summarization:
  model: "gpt-4"  # or "claude-3-opus-20240229"
  temperature: 0.3
  max_summary_length: 1000

# Bias detection thresholds
bias_detection:
  enabled: true
  min_confidence: "low"
```

### Adding News Sources

Edit `backend/config/sources.yaml`:

```yaml
sources:
  - name: "Your News Source"
    type: "rss"
    url: "https://example.com/rss"
    bias_estimate: "center"
    rationale: "Well-established, fact-focused reporting"
    enabled: true
```

## Monitoring

### Health Checks

```bash
# API health
curl https://your-domain.com/health

# Redis health
docker-compose exec redis redis-cli ping

# PostgreSQL health
docker-compose exec postgres pg_isready -U talkless
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f api
docker-compose logs -f pipeline

# View last 100 lines
docker-compose logs --tail=100 api
```

### Metrics

Monitor key metrics:
- API response times
- Pipeline execution time
- Database size
- Cache hit rate
- LLM API costs

## Troubleshooting

### Pipeline Not Running

```bash
# Check pipeline logs
docker-compose logs pipeline

# Manually trigger pipeline
docker-compose exec pipeline python backend/pipeline/run.py

# Check environment variables
docker-compose exec pipeline env | grep -E '(OPENAI|ANTHROPIC|DATABASE|REDIS)'
```

### API Not Responding

```bash
# Check API logs
docker-compose logs api

# Test internal connectivity
docker-compose exec api curl http://localhost:8000/health

# Restart API
docker-compose restart api
```

### Database Issues

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Connect to database
docker-compose exec postgres psql -U talkless -d talkless

# Check connections
docker-compose exec postgres psql -U talkless -d talkless -c "SELECT count(*) FROM pg_stat_activity;"
```

### Redis Connection Issues

```bash
# Check Redis logs
docker-compose logs redis

# Test Redis
docker-compose exec redis redis-cli ping

# Check memory usage
docker-compose exec redis redis-cli info memory
```

### Out of Memory

```bash
# Check container memory
docker stats

# Increase Docker memory limit
# Edit /etc/docker/daemon.json:
{
  "default-ulimits": {
    "memlock": {
      "Hard": -1,
      "Name": "memlock",
      "Soft": -1
    }
  }
}

# Restart Docker
sudo systemctl restart docker
```

## Security Considerations

### 1. API Keys

- **Never commit** `.env` to version control
- Rotate API keys regularly
- Use read-only API keys where possible
- Monitor API usage for anomalies

### 2. Database Security

```bash
# Use strong passwords
openssl rand -base64 32

# Restrict database access
# Edit docker-compose.yml to remove public ports in production
```

### 3. Network Security

- Use firewall rules to restrict access
- Keep services updated
- Monitor logs for suspicious activity
- Use HTTPS everywhere

### 4. AGPL v3 Compliance

Remember: Talk-Less is licensed under AGPL v3

- All modifications must be open-sourced
- If you deploy as a network service, source code must be available
- Include link to source code in API responses
- Maintain AGPL v3 license headers

### 5. Backup Strategy

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
docker-compose exec -T postgres pg_dump -U talkless talkless | gzip > backup_${DATE}.sql.gz

# Backup configuration
tar -czf config_${DATE}.tar.gz backend/config/

# Upload to secure location
# aws s3 cp backup_${DATE}.sql.gz s3://your-bucket/backups/
```

## Scaling Considerations

### Horizontal Scaling

For high traffic:

1. **Multiple API instances** behind load balancer
2. **Separate pipeline workers** for parallel processing
3. **Redis cluster** for distributed caching
4. **PostgreSQL read replicas** for query distribution

### Vertical Scaling

- Increase RAM for embedding model cache
- Use GPU instances for faster article processing
- SSD storage for database performance

## Support

- **Documentation**: https://github.com/UnaverageDeveloper/Talk-Less
- **Issues**: https://github.com/UnaverageDeveloper/Talk-Less/issues
- **License**: AGPL v3.0-or-later

---

**Remember**: Talk-Less is a public good project. No monetization, no tracking, no ads. Keep it that way.
