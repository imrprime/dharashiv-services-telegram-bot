# 🌐 How to Host Dharashiv Home Services Telegram Bot (24/7 Hosting Guide)

This guide provides simple, step-by-step instructions to host your Telegram Bot online 24/7.

---

## 🚀 Option 1: Cloud Platforms (Easiest & Free/Low Cost)

### A. Railway.app (Recommended)
1. Push your project code to **GitHub** (keep `.env` private or set variables in Railway dashboard).
2. Go to [Railway.app](https://railway.app) and sign in with GitHub.
3. Click **"New Project"** -> **"Deploy from GitHub repo"** -> Select your repo.
4. Go to **Variables** tab and add:
   - `BOT_TOKEN`: `your_bot_token`
   - `ADMIN_IDS`: `your_telegram_id`
   - `SUPPORT_PHONE`: `your_phone`
   - `SUPPORT_WHATSAPP`: `your_phone`
5. Railway will automatically detect the [Dockerfile](file:///workspace/project/Dockerfile) or Python app and start your bot 24/7!

### B. Render.com
1. Create an account at [Render.com](https://render.com).
2. Click **"New +"** -> **"Background Worker"** (Telegram polling bots run as background workers, not web services).
3. Connect your GitHub repository.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python bot.py`
6. Add your Environment Variables (`BOT_TOKEN`, `ADMIN_IDS`, etc.).
7. Click **Deploy**.

---

## 🖥️ Option 2: Linux VPS (DigitalOcean, AWS, Hetzner, Hostinger)

A VPS is ideal for business bots (starts around $3-$5 / ₹250-₹350 per month) and gives full control.

### Step 1: Upload files to your VPS
```bash
# On your server (e.g. Ubuntu 22.04 / 24.04):
mkdir -p /root/dharashiv-bot
cd /root/dharashiv-bot

# Clone your git repo or copy files:
# git clone <repo_url> .
```

### Step 2: Install dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip install -r requirements.txt
```

### Step 3: Configure `.env`
```bash
nano .env
# Paste your BOT_TOKEN and ADMIN_IDS, then press Ctrl+O, Enter, Ctrl+X to save.
```

### Step 4: Run 24/7 using Systemd (Auto-restart on reboot or crash)
Copy the provided service file:
```bash
sudo cp dharashiv-bot.service /etc/systemd/system/dharashiv-bot.service
sudo systemctl daemon-reload
sudo systemctl enable dharashiv-bot
sudo systemctl start dharashiv-bot
```

To check bot status:
```bash
sudo systemctl status dharashiv-bot
```
To view live logs:
```bash
journalctl -u dharashiv-bot -f
```

---

## 🐳 Option 3: Docker (Run with 1 Command)

If your server has Docker installed:

```bash
docker compose up -d --build
```
- To view logs: `docker compose logs -f`
- To stop: `docker compose down`

---

## 📱 Option 4: On an Android Phone via Termux (Free Local Hosting)

If you have a spare Android smartphone connected to Wi-Fi:
1. Install **Termux** from F-Droid.
2. In Termux, run:
   ```bash
   pkg update && pkg install python git -y
   git clone <your_repo_url>
   cd project
   pip install -r requirements.txt
   python bot.py
   ```
3. Acquire wake-lock in Termux (`termux-wake-lock`) so Android doesn't put the app to sleep.
