# Trade‑Bot
[![CI](https://github.com/matboone/trade-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/matboone/trade-bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-yellow)
![Node 20 LTS](https://img.shields.io/badge/Node-20.x-brightgreen)

> **MACD + Bollinger Bands back‑tester**  
> Node.js orchestrator • Python strategy engine • Zero‑to‑trades in 60 sec

---

## Key features
| What | Why it matters |
|------|----------------|
| **End‑to‑end stack** | Node wrapper spawns Python, mimicking micro‑service orchestration. |
| **Config in one line** | `npm run bot -- --symbol=SOFI --interval=m30` (m1 / m5 / m15 / m30 / h1 / d1). |
| **Test‑first mindset** | CI runs an offline smoke test on every push; green badge proves it builds. |
| **.env‑driven credentials** | No secrets in code; works locally and in cloud runners. |
| **Ready for Docker & cron** | One command away from 24/7 scheduled runs. |

---

## Quick start

```bash
# Clone
git clone https://github.com/matboone/trade-bot.git && cd trade-bot

# Python deps (virtual‑env recommended)
python -m venv .venv             # or conda/mamba
.\.venv\Scripts\activate         # Windows
pip install -r requirements.txt

# Node deps
npm ci

# Secrets
cp .env.example .env             # add your Webull creds

# 7‑day back‑test on 30‑min candles
npm run bot -- --symbol=SOFI --interval=m30
```

---

## Architecture

```mermaid
graph TD
  subgraph Node.js
    A[Node wrapper\nindex.js]
  end
  subgraph Python
    B[bot.core\n(MACD + BB)]
    C[pandas]
  end
  D[Webull API]
  A -->|spawn| B
  B --> C --> B
  B -->|HTTP| D
```

---

## Disclaimer
This project is for educational purposes only. It does not constitute financial advice, and no live orders are executed by default. Use responsibly and at your own risk.
