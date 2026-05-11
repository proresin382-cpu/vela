from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from openai import OpenAI
import os
import markdown as md
import json

app = Flask(__name__)
app.secret_key = 'vela-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vela.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Markdown filter for templates
@app.template_filter('markdown')
def markdown_filter(text):
    return md.markdown(text, extensions=['nl2br'])

# ── Models ──────────────────────────────────────────────────────────────────

class Agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clients = db.relationship('Client', backref='agency', lazy=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    agents = db.relationship('Agent', backref='client', lazy=True)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    agent_type = db.Column(db.String(50))  # receptionist, sales, support, etc
    platform = db.Column(db.String(50))    # n8n, vapi, voiceflow, custom
    status = db.Column(db.String(20), default='active')  # active, paused, error
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = db.relationship('ActivityLog', backref='agent', lazy=True)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    event_type = db.Column(db.String(50))
    summary = db.Column(db.Text)
    outcome = db.Column(db.String(20))
    source = db.Column(db.String(50), default='dashboard')  # 'dashboard' or 'external'
    source_ip = db.Column(db.String(50), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ── Auth Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'agency_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if Agency.query.filter_by(email=email).first():
            return render_template('auth.html', error='Email already registered', mode='signup')
        agency = Agency(name=name, email=email, password=generate_password_hash(password))
        db.session.add(agency)
        db.session.commit()
        session['agency_id'] = agency.id
        session['agency_name'] = agency.name
        return redirect(url_for('dashboard'))
    return render_template('auth.html', mode='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        agency = Agency.query.filter_by(email=email).first()
        if agency and check_password_hash(agency.password, password):
            session['agency_id'] = agency.id
            session['agency_name'] = agency.name
            return redirect(url_for('dashboard'))
        return render_template('auth.html', error='Invalid credentials', mode='login')
    return render_template('auth.html', mode='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ── Dashboard ────────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    agency_id = session['agency_id']
    clients = Client.query.filter_by(agency_id=agency_id).all()
    total_agents = sum(len(c.agents) for c in clients)
    total_logs = ActivityLog.query.join(Agent).join(Client).filter(Client.agency_id == agency_id).count()
    active_agents = Agent.query.join(Client).filter(Client.agency_id == agency_id, Agent.status == 'active').count()
    recent_logs = ActivityLog.query.join(Agent).join(Client).filter(
        Client.agency_id == agency_id
    ).order_by(ActivityLog.created_at.desc()).limit(10).all()
    return render_template('dashboard.html',
        clients=clients,
        total_agents=total_agents,
        total_logs=total_logs,
        active_agents=active_agents,
        recent_logs=recent_logs
    )

# ── Clients ──────────────────────────────────────────────────────────────────

@app.route('/clients')
def clients():
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    clients = Client.query.filter_by(agency_id=session['agency_id']).all()
    return render_template('clients.html', clients=clients)

@app.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            business_type=request.form['business_type'],
            email=request.form['email'],
            phone=request.form['phone'],
            agency_id=session['agency_id']
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('clients'))
    return render_template('add_client.html')

@app.route('/clients/<int:client_id>/delete', methods=['POST'])
def delete_client(client_id):
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    # Delete all logs and agents first
    for agent in client.agents:
        ActivityLog.query.filter_by(agent_id=agent.id).delete()
        db.session.delete(agent)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients'))

@app.route('/agents/<int:agent_id>/delete', methods=['POST'])
def delete_agent(agent_id):
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    agent = Agent.query.get_or_404(agent_id)
    client_id = agent.client_id
    ActivityLog.query.filter_by(agent_id=agent_id).delete()
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('client_detail', client_id=client_id))

@app.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.name = request.form['name']
        client.business_type = request.form['business_type']
        client.email = request.form['email']
        client.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('client_detail', client_id=client_id))
    return render_template('edit_client.html', client=client)

@app.route('/clients/<int:client_id>')
def client_detail(client_id):
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    return render_template('client_detail.html', client=client)

# ── Agents ───────────────────────────────────────────────────────────────────

@app.route('/clients/<int:client_id>/agents/add', methods=['GET', 'POST'])
def add_agent(client_id):
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        agent = Agent(
            name=request.form['name'],
            agent_type=request.form['agent_type'],
            platform=request.form['platform'],
            description=request.form['description'],
            client_id=client_id
        )
        db.session.add(agent)
        db.session.commit()
        flash('Agent deployed successfully!', 'success')
        return redirect(url_for('client_detail', client_id=client_id))
    return render_template('add_agent.html', client=client)

@app.route('/agents/<int:agent_id>/log', methods=['POST'])
def add_log(agent_id):
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    data = request.json
    log = ActivityLog(
        agent_id=agent_id,
        event_type=data.get('event_type', 'conversation'),
        summary=data.get('summary', ''),
        outcome=data.get('outcome', 'success')
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/agents/<int:agent_id>/status', methods=['POST'])
def update_status(agent_id):
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    agent = Agent.query.get_or_404(agent_id)
    data = request.json
    agent.status = data.get('status', agent.status)
    db.session.commit()
    return jsonify({'success': True})

# ── AI Report Generation ─────────────────────────────────────────────────────

@app.route('/clients/<int:client_id>/report', methods=['GET', 'POST'])
def generate_report(client_id):
    if 'agency_id' not in session:
        return redirect(url_for('login'))
    client = Client.query.get_or_404(client_id)
    report = None
    if request.method == 'POST':
        api_key = request.form.get('api_key') or os.getenv('GEMINI_API_KEY')
        logs = ActivityLog.query.join(Agent).filter(Agent.client_id == client_id).order_by(ActivityLog.created_at.desc()).limit(50).all()
        log_summary = []
        for log in logs:
            log_summary.append(f"[{log.created_at.strftime('%Y-%m-%d %H:%M')}] {log.event_type.upper()} — {log.summary} (Outcome: {log.outcome})")
        agents_info = []
        for agent in client.agents:
            agents_info.append(f"Agent: {agent.name} | Type: {agent.agent_type} | Platform: {agent.platform} | Status: {agent.status}")
        prompt = f"""You are a professional AI agency analyst. Generate a clean, professional client performance report for the following client.

Client: {client.name}
Business Type: {client.business_type}

Deployed Agents:
{chr(10).join(agents_info) if agents_info else 'No agents deployed yet'}

Recent Activity Logs (last 50 events):
{chr(10).join(log_summary) if log_summary else 'No activity logged yet'}

Write a professional report with these sections:
1. Executive Summary
2. Agent Performance Overview
3. Key Metrics & Highlights
4. Issues or Alerts (if any)
5. Recommendations for Next Month

Keep it concise, professional, and actionable. Format it clearly."""

        try:
            import urllib.request
            import json as json_lib
            # Try Gemini first
            gemini_key = api_key
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = json_lib.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json_lib.loads(resp.read().decode('utf-8'))
                report = data['candidates'][0]['content']['parts'][0]['text']
        except Exception as gemini_error:
            # Fallback to OpenAI if Gemini fails
            try:
                from openai import OpenAI
                openai_key = os.getenv('OPENAI_API_KEY', '')
                if openai_key:
                    ai = OpenAI(api_key=openai_key)
                    response = ai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1500
                    )
                    report = response.choices[0].message.content
                else:
                    report = f"Error generating report: {str(gemini_error)}"
            except Exception as e:
                report = f"Error generating report: {str(e)}"

    return render_template('report.html', client=client, report=report)

# ── Webhook (for real agent platforms to push logs) ──────────────────────────

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/early-access', methods=['GET', 'POST'])
def early_access():
    submitted = False
    if request.method == 'POST':
        submitted = True
    return render_template('early_access.html', submitted=submitted)

@app.route('/analytics/events')
def analytics_events():
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    from datetime import timedelta
    agency_id = session['agency_id']
    labels = []
    counts = []
    for i in range(6, -1, -1):
        day = datetime.utcnow() - timedelta(days=i)
        label = day.strftime('%b %d')
        start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end = day.replace(hour=23, minute=59, second=59)
        count = ActivityLog.query.join(Agent).join(Client).filter(
            Client.agency_id == agency_id,
            ActivityLog.created_at >= start,
            ActivityLog.created_at <= end
        ).count()
        labels.append(label)
        counts.append(count)
    return jsonify({'labels': labels, 'counts': counts})

@app.route('/agents/<int:agent_id>/toggle', methods=['POST'])
def toggle_agent(agent_id):
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    agent = Agent.query.get_or_404(agent_id)
    if agent.status == 'active':
        agent.status = 'paused'
    elif agent.status == 'paused':
        agent.status = 'active'
    else:
        agent.status = 'active'
    db.session.commit()
    return jsonify({'success': True, 'status': agent.status})

@app.route('/agents/<int:agent_id>/test-webhook', methods=['POST'])
def test_webhook(agent_id):
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    import random
    samples = [
        ('conversation', 'Patient called asking about appointment availability', 'success'),
        ('booking', 'New appointment booked for next Tuesday at 2PM', 'success'),
        ('conversation', 'Client inquiry about pricing and services', 'success'),
        ('handoff', 'Call transferred to human agent successfully', 'success'),
        ('booking', 'Appointment rescheduled per client request', 'success'),
        ('conversation', 'FAQ answered about business hours', 'success'),
        ('error', 'Failed to connect to calendar service', 'failed'),
        ('conversation', 'New lead captured with contact details', 'success'),
        ('booking', 'Follow-up call scheduled for tomorrow', 'success'),
        ('conversation', 'Customer complaint handled and escalated', 'success'),
    ]
    sample = random.choice(samples)
    log = ActivityLog(
        agent_id=agent_id,
        event_type=sample[0],
        summary=sample[1],
        outcome=sample[2]
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({
        'success': True,
        'event_type': sample[0],
        'summary': sample[1],
        'outcome': sample[2]
    })

@app.route('/webhook/<int:agent_id>', methods=['POST'])
def webhook(agent_id):
    data = request.json or {}
    # Get real IP - check for proxy headers first
    source_ip = request.headers.get('X-Real-IP') or \
                request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
                request.remote_addr or ''
    # Determine if external (not from our own server)
    internal_ips = ['127.0.0.1', 'localhost', '::1']
    is_external = source_ip not in internal_ips
    source = 'external' if is_external else 'dashboard'
    log = ActivityLog(
        agent_id=agent_id,
        event_type=data.get('event_type', 'conversation'),
        summary=data.get('summary', ''),
        outcome=data.get('outcome', 'success'),
        source=source,
        source_ip=source_ip
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'received': True})

@app.route('/agents/<int:agent_id>/connection-status')
def connection_status(agent_id):
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    # Check for any external webhook calls
    external_log = ActivityLog.query.filter_by(
        agent_id=agent_id,
        source='external'
    ).order_by(ActivityLog.created_at.desc()).first()
    if external_log:
        return jsonify({
            'connected': True,
            'last_received': external_log.created_at.strftime('%b %d, %H:%M'),
            'source_ip': external_log.source_ip,
            'total_external': ActivityLog.query.filter_by(agent_id=agent_id, source='external').count()
        })
    return jsonify({'connected': False})

@app.route('/agents/<int:agent_id>/disconnect', methods=['POST'])
def disconnect_agent(agent_id):
    if 'agency_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    # Mark all external logs as dashboard source (effectively disconnects)
    ActivityLog.query.filter_by(agent_id=agent_id, source='external').update({'source': 'disconnected'})
    db.session.commit()
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
