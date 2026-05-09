import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Agency, Client, Agent, ActivityLog
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

with app.app_context():

    # Find existing agency or create demo one
    agency = Agency.query.first()
    if not agency:
        agency = Agency(
            name='Orrin Agency',
            email='ali@orrin.agency',
            password=generate_password_hash('demo1234')
        )
        db.session.add(agency)
        db.session.commit()
        print(f'Created agency: {agency.name}')
    else:
        print(f'Using existing agency: {agency.name}')

    # Demo clients
    clients_data = [
        {'name': 'Dr. Smith Dental Clinic', 'business_type': 'Dental Clinic', 'email': 'drsmith@clinic.com', 'phone': '+1 555 100 2000'},
        {'name': 'LegalEase Law Firm', 'business_type': 'Law Firm', 'email': 'contact@legalease.com', 'phone': '+1 555 200 3000'},
        {'name': 'FitLife Gym', 'business_type': 'Fitness Center', 'email': 'info@fitlife.com', 'phone': '+1 555 300 4000'},
        {'name': 'RealtyPro Agency', 'business_type': 'Real Estate', 'email': 'hello@realtypro.com', 'phone': '+1 555 400 5000'},
    ]

    agents_data = [
        [
            {'name': 'Reception Bot', 'agent_type': 'receptionist', 'platform': 'vapi', 'status': 'active', 'description': 'Handles incoming calls and books appointments'},
            {'name': 'Appointment Reminder', 'agent_type': 'follow_up', 'platform': 'n8n', 'status': 'active', 'description': 'Sends automated appointment reminders'},
        ],
        [
            {'name': 'Client Intake Bot', 'agent_type': 'support', 'platform': 'voiceflow', 'status': 'active', 'description': 'Handles initial client inquiries and case intake'},
        ],
        [
            {'name': 'Membership Sales Agent', 'agent_type': 'sales', 'platform': 'n8n', 'status': 'active', 'description': 'Qualifies leads and sells gym memberships'},
            {'name': 'Class Booking Bot', 'agent_type': 'booking', 'platform': 'vapi', 'status': 'paused', 'description': 'Books fitness classes for members'},
        ],
        [
            {'name': 'Lead Qualifier', 'agent_type': 'lead_qualifier', 'platform': 'voiceflow', 'status': 'active', 'description': 'Qualifies property buyer and seller leads'},
            {'name': 'Property Info Bot', 'agent_type': 'support', 'platform': 'n8n', 'status': 'error', 'description': 'Answers property listing questions'},
        ],
    ]

    log_templates = [
        ('conversation', 'Patient called to book appointment for teeth cleaning', 'success'),
        ('booking', 'Appointment booked for May 15 at 10:00 AM', 'success'),
        ('conversation', 'Caller asked about pricing for dental implants', 'success'),
        ('booking', 'Appointment rescheduled from May 12 to May 18', 'success'),
        ('conversation', 'Patient inquiry about insurance coverage', 'success'),
        ('handoff', 'Call transferred to human receptionist', 'success'),
        ('conversation', 'Answered FAQ about clinic opening hours', 'success'),
        ('booking', 'Appointment cancelled per patient request', 'success'),
        ('error', 'Failed to connect to calendar API', 'failed'),
        ('conversation', 'New client inquiry — captured contact details', 'success'),
        ('conversation', 'Lead qualified — high intent buyer', 'success'),
        ('booking', 'Viewing scheduled for 45 Oak Street', 'success'),
        ('conversation', 'Membership upgrade inquiry handled', 'success'),
        ('booking', 'Yoga class booked for Saturday 9AM', 'success'),
        ('conversation', 'Client asked about payment plans', 'success'),
    ]

    created_clients = []
    for i, cdata in enumerate(clients_data):
        # Check if client already exists
        existing = Client.query.filter_by(name=cdata['name'], agency_id=agency.id).first()
        if existing:
            created_clients.append(existing)
            print(f'Client already exists: {cdata["name"]}')
            continue

        client = Client(agency_id=agency.id, **cdata)
        db.session.add(client)
        db.session.commit()
        created_clients.append(client)
        print(f'Created client: {client.name}')

        for adata in agents_data[i]:
            agent = Agent(client_id=client.id, **adata)
            db.session.add(agent)
            db.session.commit()
            print(f'  Created agent: {agent.name} ({agent.status})')

            # Add activity logs going back 7 days
            if agent.status != 'error':
                num_logs = random.randint(8, 15)
                for j in range(num_logs):
                    template = random.choice(log_templates)
                    log = ActivityLog(
                        agent_id=agent.id,
                        event_type=template[0],
                        summary=template[1],
                        outcome=template[2],
                        created_at=datetime.utcnow() - timedelta(
                            days=random.randint(0, 7),
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59)
                        )
                    )
                    db.session.add(log)
                db.session.commit()
                print(f'    Added {num_logs} activity logs')

    print('\n✅ Demo data seeded successfully!')
    print(f'Clients: {len(created_clients)}')
    total_agents = sum(len(c.agents) for c in created_clients)
    print(f'Total agents: {total_agents}')
    print('\nRestart server and refresh dashboard to see the data.')
