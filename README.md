# Vela — AI Agency Command Center

![Status](https://img.shields.io/badge/Status-Live-4DFFC3?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0-white?style=for-the-badge)
![Hackathon](https://img.shields.io/badge/AI_Agent_Olympics-2026-7B61FF?style=for-the-badge)
![Live](https://img.shields.io/badge/Live_at-tryvela.io-4DFFC3?style=for-the-badge)

> **Your agents are live. Are you watching them?**

## 🌐 Live Demo

**[tryvela.io](https://tryvela.io)** — Live on Vultr with SSL

Demo account: `demo@tryvela.io` / `demo1234`

## 🚀 What is Vela?

Vela is the operations platform built for AI agencies. Once you deploy AI agents for clients, you need visibility — are they working? Are they failing? Is your client happy?

Vela gives you one dashboard to manage every client, monitor every agent, and understand exactly what's happening in real time.

## ✨ Features

- **Client Management** — Add, edit, delete clients
- **Agent Monitoring** — Real-time status for every deployed agent
- **Live Webhooks** — Connect any agent platform via unique webhook URL
- **Connection Detection** — Know when an agent connects with source IP tracking
- **Activity Logs** — Every event logged automatically with timestamps
- **AI Reports** — One-click professional reports powered by GPT-4o mini
- **Agent Controls** — Pause, activate, or disconnect agents instantly
- **Pricing Plans** — 3-tier pricing with 16-day free trial
- **Mobile Responsive** — Full mobile UI with hamburger navigation
- **Webhook Setup Wizard** — Step-by-step guides for n8n, Vapi, Make, cURL, Python

## 🔗 Webhook Integration

Each agent gets a unique webhook URL:
```
POST https://tryvela.io/webhook/{agent_id}
```

Send events from any platform:
```json
{
  "event_type": "conversation",
  "summary": "Patient called to book appointment",
  "outcome": "success"
}
```

Supported: n8n, Vapi, Voiceflow, Make, Bland AI, or any custom platform.

## 🛠 Tech Stack

- **Backend:** Python 3.12 + Flask
- **Database:** SQLite via SQLAlchemy
- **AI:** OpenAI GPT-4o mini
- **Hosting:** Vultr Ubuntu 24.04
- **Server:** Gunicorn + Nginx
- **SSL:** Let's Encrypt

## 🚀 Quick Start

```bash
git clone https://github.com/proresin382-cpu/vela.git
cd vela
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
python app.py
```

## 🏆 Hackathon

Built for **AI Agent Olympics 2026** and **TECHEX Hackathon 2026** on lablab.ai

- Track: Agent Monitoring & Observability
- Deployed on: Vultr
- Built by: Ali Mehdi, Founder of Orrin Agency, Lahore 🇵🇰

## 📬 Contact

- Website: [orrin.agency](https://orrin.agency)
- Instagram: [@orrin.agency](https://instagram.com/orrin.agency)
- Vela: [tryvela.io](https://tryvela.io)
- Vela Instagram: [@app.vela](https://instagram.com/app.vela)
