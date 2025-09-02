#!/usr/bin/env python3
"""
F1 Racer AI Agent - Flask Web Interface

This Flask application provides a professional web interface for the F1 AI Agent,
mirroring all CLI functionality while maintaining the original command-line interface.

Features:
- Agent configuration
- Message generation (Speak)
- Social media actions (Act)
- Context management (Think)
- Race weekend simulation
- Clean, responsive design

Author: F1 AI Agent Web Interface
Date: 2025
"""

from flask import Flask, render_template, request, jsonify, session, redirect
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import traceback

# Import F1 Agent and related modules
from f1_agent import F1Agent, create_f1_agent, MessageType, ContextState, SessionType
from f1_data import F1_TEAMS, F1_CIRCUITS, RACE_WEEKEND_SESSIONS

app = Flask(__name__)
app.secret_key = 'f1-racer-ai-agent-2025'

# Store agents by session ID
agents: Dict[str, F1Agent] = {}

def get_session_id() -> str:
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_agent() -> Optional[F1Agent]:
    """Get agent for current session"""
    session_id = get_session_id()
    return agents.get(session_id)

def set_agent(agent: F1Agent) -> None:
    """Set agent for current session"""
    session_id = get_session_id()
    agents[session_id] = agent

@app.route('/')
def index():
    """Main page - agent configuration or dashboard"""
    agent = get_agent()
    if agent:
        return render_template('dashboard.html', 
                             agent_configured=True,
                             driver_name=agent.context.driver_name,
                             team_name=agent.context.team)
    else:
        return render_template('index.html', 
                             teams=F1_TEAMS,
                             circuits=list(F1_CIRCUITS.keys()))

@app.route('/configure', methods=['POST'])
def configure_agent():
    """Configure the F1 Agent"""
    try:
        data = request.get_json()
        driver_name = data.get('driver_name', 'Alex Driver')
        team_key = data.get('team_key', 'mclaren')
        circuit_key = data.get('circuit_key', 'silverstone')
        weekend_type = data.get('weekend_type', 'standard_weekend')
        
        # Validate inputs
        if team_key not in F1_TEAMS:
            return jsonify({'success': False, 'error': f'Invalid team: {team_key}'})
        
        if circuit_key not in F1_CIRCUITS:
            circuit_key = 'silverstone'
        
        # Create agent
        agent = create_f1_agent(driver_name, team_key)
        
        # Set initial context
        agent.think_update_context(
            current_circuit=circuit_key,
            weekend_type=weekend_type,
            current_state=ContextState.PRE_WEEKEND
        )
        
        set_agent(agent)
        
        return jsonify({
            'success': True,
            'driver_name': driver_name,
            'team_name': F1_TEAMS[team_key].name,
            'circuit': F1_CIRCUITS[circuit_key].name
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dashboard')
def dashboard():
    """Agent dashboard"""
    agent = get_agent()
    if not agent:
        return redirect('/')
    
    return render_template('dashboard.html',
                         agent_configured=True,
                         driver_name=agent.context.driver_name,
                         team_name=agent.context.team)

@app.route('/speak', methods=['POST'])
def speak():
    """Generate message (Speak capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        message_type = MessageType(data.get('message_type', 'post'))
        custom_context = data.get('custom_context') or ''
        custom_context = custom_context.strip() if custom_context else None
        
        message = agent.speak(message_type, custom_context)
        
        return jsonify({
            'success': True,
            'message': message,
            'message_type': message_type.value,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/act/post', methods=['POST'])
def act_post():
    """Post status update (Act capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        custom_content = data.get('content') or ''
        custom_content = custom_content.strip() if custom_content else None
        
        action = agent.act_post_status(custom_content)
        
        return jsonify({
            'success': True,
            'content': action.content,
            'engagement': action.metadata.get('engagement', 0),
            'timestamp': action.timestamp.isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/act/reply', methods=['POST'])
def act_reply():
    """Reply to fan comment (Act capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        fan_comment = data.get('fan_comment') or ''
        fan_comment = fan_comment.strip() if fan_comment else ''
        
        if not fan_comment:
            return jsonify({'success': False, 'error': 'No fan comment provided'})
        
        action = agent.act_reply_to_comment(fan_comment)
        
        return jsonify({
            'success': True,
            'reply': action.content,
            'original_comment': fan_comment,
            'sentiment': action.metadata.get('original_sentiment', 'unknown'),
            'timestamp': action.timestamp.isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/act/like', methods=['POST'])
def act_like():
    """Like a post (Act capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        post_content = data.get('post_content') or ''
        post_content = post_content.strip() if post_content else ''
        
        if not post_content:
            return jsonify({'success': False, 'error': 'No post content provided'})
        
        action = agent.act_like_post(post_content)
        
        return jsonify({
            'success': True,
            'liked_post': post_content[:100] + ('...' if len(post_content) > 100 else ''),
            'timestamp': action.timestamp.isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/act/mention', methods=['POST'])
def act_mention():
    """Mention someone (Act capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        person_name = data.get('person_name') or ''
        person_name = person_name.strip() if person_name else ''
        context = data.get('context') or 'general'
        context = context.strip() if context else 'general'
        
        if not person_name:
            return jsonify({'success': False, 'error': 'No person name provided'})
        
        action = agent.act_mention_someone(person_name, context)
        
        return jsonify({
            'success': True,
            'content': action.content,
            'mentioned_person': person_name,
            'context': context,
            'timestamp': action.timestamp.isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/think/context')
def think_context():
    """Show current context (Think capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        context = agent.think_show_context()
        
        return jsonify({
            'success': True,
            'context': context
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/think/update', methods=['POST'])
def think_update():
    """Update context (Think capability)"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        updates = {}
        
        # Process updates
        if data.get('circuit') and data['circuit'] in F1_CIRCUITS:
            updates['current_circuit'] = data['circuit']
        
        if data.get('session'):
            try:
                updates['current_session'] = SessionType(data['session'])
            except ValueError:
                pass
        
        if data.get('mood') and data['mood'] in ['ecstatic', 'satisfied', 'neutral', 'disappointed', 'frustrated']:
            updates['mood'] = data['mood']
        
        if updates:
            success = agent.think_update_context(**updates)
            if success:
                # Convert enum objects to their values for JSON serialization
                serializable_updates = {}
                for key, value in updates.items():
                    if hasattr(value, 'value'):  # Handle enum objects
                        serializable_updates[key] = value.value
                    else:
                        serializable_updates[key] = value
                return jsonify({'success': True, 'updates': serializable_updates})
            else:
                return jsonify({'success': False, 'error': 'Failed to update context'})
        else:
            return jsonify({'success': False, 'error': 'No valid updates provided'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/simulation', methods=['POST'])
def run_simulation():
    """Run race weekend simulation"""
    try:
        agent = get_agent()
        if not agent:
            return jsonify({'success': False, 'error': 'Agent not configured'})
        
        data = request.get_json()
        circuit_key = data.get('circuit_key', agent.context.current_circuit)
        weekend_type = data.get('weekend_type', 'standard_weekend')
        
        if circuit_key not in F1_CIRCUITS:
            circuit_key = agent.context.current_circuit
        
        results = agent.run_race_weekend_simulation(circuit_key, weekend_type)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data/teams')
def api_teams():
    """API endpoint for team data"""
    return jsonify({team_key: {
        'name': team.name,
        'short_name': team.short_name,
        'drivers': team.drivers,
        'engine': team.engine,
        'colors': team.colors
    } for team_key, team in F1_TEAMS.items()})

@app.route('/api/data/circuits')
def api_circuits():
    """API endpoint for circuit data"""
    return jsonify({circuit_key: {
        'name': circuit.name,
        'country': circuit.country,
        'city': circuit.city,
        'length_km': circuit.length_km,
        'characteristics': circuit.characteristics
    } for circuit_key, circuit in F1_CIRCUITS.items()})

@app.route('/api/agent/status')
def api_agent_status():
    """API endpoint for agent status"""
    agent = get_agent()
    if agent:
        return jsonify({
            'configured': True,
            'driver_name': agent.context.driver_name,
            'team': agent.context.team,
            'current_circuit': agent.context.current_circuit,
            'current_session': agent.context.current_session.value if agent.context.current_session else None,
            'mood': agent.context.mood,
            'actions_performed': len(agent.action_history)
        })
    else:
        return jsonify({'configured': False})

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)