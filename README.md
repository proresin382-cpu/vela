# Vela — AI Agency Command Center

> The operations platform built for AI agencies. Monitor clients, manage agents, and auto-generate reports — all from one dashboard.

![Vela Dashboard](https://img.shields.io/badge/Status-Live-4DFFC3?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0-white?style=for-the-badge)
![Hackathon](https://img.shields.io/badge/AI_Agent_Olympics-2026-7B61FF?style=for-the-badge)
![Live](https://img.shields.io/badge/Live_at-tryvela.io-4DFFC3?style=for-the-badge)

---

## 🌐 Live Demo

**[tryvela.io](http://tryvela.io)** — Live on Vultr, deployed tonight

> Built by an FA student from Lahore, Pakistan with zero CS degree — in one Saturday night at the AI Agent Olympics Hackathon 2026.

AI agencies are growing fast — but they have no proper infrastructure to manage the agents they deploy for clients.

Agencies are currently:
- Tracking agent activity in spreadsheets
- Writing client reports manually every month
- Having no visibility into whether agents are working or broken
- Juggling multiple platforms with no central view

**Vela solves this.**

Vela is a SaaS platform that gives AI agencies a single command center to:
- Manage all their clients in one place
- Deploy and monitor AI agents per client
- Receive real-time activity logs via webhooks from any platform
- Generate professional AI-powered client reports in one click
- Track agent performance over time with analytics

---

## 🎯 Hackathon Tracks

This project targets the following tracks at the **AI Agent Olympics Hackathon 2026**:

- ✅ **Enterprise Utility** — Solves a real operational pain point for AI agencies
- ✅ **Agentic Workflows** — AI generates structured client reports from agent activity data
- ✅ **Vultr Deployment** — Deployed on Vultr cloud infrastructure

---

## ✨ Features

### Client Management
- Add and manage unlimited clients
- Track business type, contact info, and deployment date
- View all agents per client at a glance

### Agent Monitoring
- Deploy agents per client with type and platform tracking
- Real-time status monitoring (Active / Paused / Error)
- One-click status toggle — pause or activate any agent instantly

### Activity Logs & Webhooks
- Every agent event logged automatically
- Universal webhook endpoint for any platform
- Connect n8n, Vapi, Voiceflow, Make, Bland AI or any custom system
- Test webhook button for live demo and testing

### AI Report Generation
- One-click professional client performance reports
- Powered by GPT-4o mini
- Covers: Executive Summary, Agent Performance, Key Metrics, Issues, Recommendations
- Rendered in clean markdown with print/PDF support

### Analytics Dashboard
- 7-day activity chart per agency
- Real-time stats: clients, agents, active agents, total events
- Recent activity feed across all agents

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + Flask |
| Database | SQLite (PostgreSQL ready) |
| AI | OpenAI GPT-4o mini |
| Frontend | HTML + CSS + Vanilla JS |
| Charts | Chart.js |
| Deployment | Vultr |

---

## 🔗 Webhook Integration

Any agent platform can push data to Vela via a simple POST request:

```bash
POST https://yourdomain.com/webhook/{agent_id}

{
  "event_type": "booking",
  "summary": "Appointment booked for May 15 at 10AM",
  "outcome": "success"
}
```

### Supported Platforms
| Platform | Integration Method |
|----------|------------------|
| n8n | HTTP Request node at workflow end |
| Vapi | Webhook in call end trigger |
| Voiceflow | API block at conversation end |
| Make | HTTP module |
| Bland AI | Webhook on call complete |
| Custom | Direct API call |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/vela.git
cd vela

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open your browser at `http://localhost:5000`

### First Steps
1. Sign up with your agency name and email
2. Add your first client
3. Deploy an agent for that client
4. Use the webhook endpoint to connect your agent platform
5. Generate an AI report to send to your client

---

## 📁 Project Structure

```
vela/
├── app.py                 # Flask application + all routes
├── requirements.txt       # Python dependencies
├── instance/
│   └── vela.db           # SQLite database (auto-created)
└── templates/
    ├── base.html          # Base layout with sidebar
    ├── landing.html       # Public landing page
    ├── auth.html          # Login / Signup
    ├── dashboard.html     # Main dashboard
    ├── clients.html       # Clients list
    ├── client_detail.html # Client + agents view
    ├── add_client.html    # Add client form
    ├── add_agent.html     # Add agent form
    └── report.html        # AI report generation
```

---

## 🗺 Roadmap

- [ ] Native n8n integration
- [ ] Native Vapi integration
- [ ] Native Voiceflow integration
- [ ] Email report delivery to clients
- [ ] Multi-user agency teams
- [ ] Custom branding per client portal
- [ ] PostgreSQL for production
- [ ] Usage-based pricing tiers

---

## 💰 Business Model

Vela is built as a standalone SaaS product for AI agencies:

| Plan | Price | Clients | Agents |
|------|-------|---------|--------|
| Starter | $49/mo | 5 | 10 |
| Growth | $99/mo | 20 | 50 |
| Agency | $199/mo | Unlimited | Unlimited |

---

## 👨‍💻 Built By

Built at the **AI Agent Olympics Hackathon 2026** — Milan AI Week.

**Orrin Agency** — We build AI agents for businesses.
- Website: [orrin.agency](https://orrin.agency)
- Instagram: [@orrin.agency](https://instagram.com/orrin.agency)
- Vela: [tryvela.io](http://tryvela.io)
- Vela Instagram: [@app.vela](https://instagram.com/app.vela)

---

## 📄 License

MIT License — free to use, modify, and deploy.
