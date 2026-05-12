# Vela — AI Agency Command Center

![Status](https://img.shields.io/badge/Status-Live-4DFFC3?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0-white?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?style=for-the-badge)
![Vultr](https://img.shields.io/badge/Deployed-Vultr-007BFC?style=for-the-badge)
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
- **AI Reports** — One-click professional reports powered by **Gemini 2.5 Flash**
- **Agent Controls** — Pause, activate, or disconnect agents instantly
- **Security Audit** — Every AI interaction inspected by Lobster Trap security proxy
- **Pricing Plans** — 3-tier pricing ($49/$99/$199/mo) with 16-day free trial
- **Mobile Responsive** — Full mobile UI with hamburger navigation
- **Webhook Setup Wizard** — Step-by-step guides for n8n, Vapi, Make, cURL, Python

## 🔒 Security — Powered by Veea Lobster Trap

Every AI report generation is protected by **[Lobster Trap](https://github.com/veeainc/lobstertrap)** — Veea's enterprise security proxy.

- **Prompt injection detection** — blocks attempts to manipulate AI behavior
- **PII exfiltration guard** — prevents exposure of sensitive data
- **Risk scoring** — every request scored 0.0–1.0 for security risk
- **Audit trails** — full log of every AI interaction with metadata
- **Intent mismatch detection** — flags when detected behavior differs from declared intent
- **Real-time dashboard** — visible at `tryvela.io/security`

```
Lobster Trap sits between Vela and Gemini API
Every prompt → inspected → risk scored → logged → forwarded
```

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
- **AI:** Google Gemini 2.5 Flash (via OpenAI-compatible endpoint)
- **Security:** Veea Lobster Trap (prompt inspection + audit logging)
- **Hosting:** Vultr Ubuntu 24.04
- **Server:** Gunicorn + Nginx
- **SSL:** Let's Encrypt

## 🚀 Quick Start

```bash
git clone https://github.com/proresin382-cpu/vela.git
cd vela
pip install -r requirements.txt
export GEMINI_API_KEY=your_gemini_key_here
python app.py
```

## 🏆 Hackathon

Built for **AI Agent Olympics 2026** and **TECHEX Hackathon 2026** on lablab.ai

- **AI Agent Olympics tracks:** Enterprise Utility + Vultr Award
- **TECHEX tracks:** Track 1 (Agent Security & AI Governance — Veea) + Track 2 (Google AI Studio — Gemini)
- **Deployed on:** Vultr
- **AI:** Google Gemini 2.5 Flash
- **Security:** Veea Lobster Trap
- **Built by:** Ali Mehdi, Founder of Orrin Agency, Lahore 🇵🇰

## 📬 Contact

- Website: [orrin.agency](https://orrin.agency)
- Instagram: [@orrin.agency](https://instagram.com/orrin.agency)
- Vela: [tryvela.io](https://tryvela.io)
- Vela Instagram: [@app.vela](https://instagram.com/app.vela)
