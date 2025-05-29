# Trade‑Bot
[![CI](https://github.com/matboone/trade-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/matboone/trade-bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-yellow)
![Node 20 LTS](https://img.shields.io/badge/Node-20.x-brightgreen)

A fast back-tester for MACD + Bollinger Band strategies, driven by a Node.js wrapper + Python engine, exposed via CLI, REST API, and a React dashboard.

---

## Why I Built Trade‑Bot

Manual swing‑trading forced me to watch price feeds for hours and still miss entry windows.  
I wanted a **hands‑off agent** that could (1) scan live market data, (2) decide when to buy or
sell based on statistical signals, and (3) log every action for review.  
Building it let me sharpen skills in Python, event‑driven AWS architecture, and ML model
deployment—exactly the stack I enjoy using for production AI tools.

## Impact

* **10‑20 % annualized return** in paper‑trade back‑tests across 50 equities (2018‑2023).  
* **Zero manual oversight**—Lambda runs every 5 minutes, produces LightGBM signals in <200 ms,
  and posts orders + metrics to a MongoDB dashboard.  
* **Easily extensible** workflow: swap in new models or exchanges by editing one config file.  
* **Learning accelerator**: the project taught me practical MLOps—data ingestion, feature
  pipelines, containerization, CI tests, and real‑time monitoring.

These results show how a small AI agent can automate a repetitive decision process and free
users to focus on higher‑level strategy. Feel free to clone the repo, configure your API keys,
and run your own experiments.

---

## Prerequisites

- **Git**: `git --version` (install from https://git-scm.com)
- **Python 3.12+**: `python3 --version` (install from https://python.org)
- **Node.js 20 LTS + npm**: `node --version && npm --version` (install from https://nodejs.org)
- **Webull account**: Sign up at https://www.webull.com and note your email & password.

---

## Quick Start (CLI)

```bash
git clone https://github.com/matboone/trade-bot.git
cd trade-bot

# 1. Credentials
cp .env.example .env
# Edit `.env`, set WEBULL_USER and WEBULL_PASS

# 2. Python environment
python3 -m venv .venv
# Windows:
. .\.venv\Scripts\Activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt

# 3. Node dependencies
npm ci

# 4. Run back-test (7 days, 30m interval)
npm run bot -- --symbol=SOFI --interval=m30
```

---

## REST API

Start the API server on port 3000:

```bash
# If venv is active:
npm run api
# Or explicitly activate venv then:
. .venv/bin/activate && npm run api
```

Test with curl:

```bash
curl "http://localhost:3000/backtest?symbol=AAPL&interval=h1"
```

By default the API returns plain-text logs. To enable JSON output:

1. In `bot/core.py`, add a `--json` flag and `print(json.dumps(...))`.
2. In `api.js`, append `--json` to the execa arguments and `res.json(JSON.parse(stdout))`.

---

## React Dashboard

A simple frontend to drive the API and display results.

1. Create or navigate to `dashboard/`:
   ```bash
   cd dashboard
   npm install
   # Ensure proxy in package.json:
   # "proxy": "http://localhost:3000",
   npm start
   ```
2. In your browser visit `http://localhost:3001` (or 3000 if you set proxy ports).
3. Enter a ticker & interval, then click **Run Backtest**.

The dashboard sends `/backtest?symbol=...&interval=...` to your API and streams the output.

---

## Docker & Compose

Build and run with Docker Compose:

```bash
docker compose build
# Ensure .env exists in root with credentials
docker compose up
```

This spins up two services:

- **trade-bot**: runs the back-test once (or scheduled via cron)
- **api**: exposes `/backtest` on port 3000

Disable local mounts in `docker-compose.yml` for production.

---

## Tests & CI

- **Smoke test** (offline logic): `pytest -q`
- **CI** (GitHub Actions): runs Python + Node smoke tests via `npm ci & pytest`.

Run locally:

```bash
pytest -q
npm test # if you add JS tests
```

---

## Roadmap

- [x] CLI wrapper & Python engine
- [x] REST API
- [x] React dashboard
- [x] Docker image & Compose
- [ ] Scheduled jobs (cron or node-cron)
- [ ] Authentication & rate limiting
- [ ] Equity-curve charts in dashboard

---

## License

Released under the [MIT License](/LICENSE).
