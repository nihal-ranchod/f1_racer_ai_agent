#!/usr/bin/env python3
"""
F1 Racer AI Agent - Main Implementation

This module contains the F1Agent class that simulates the persona and behavior
of a Formula One racer for social media interactions.

Features:
- Speak (Generate Text): Generate F1 racer-style messages and posts
- Act (Perform Actions): Simulate social media actions (post, reply, like, mention)
- Think (Contextual Awareness): Maintain race weekend context and adapt responses

Author: F1 AI Agent Assessment
Date: 2025
"""

import random
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Import F1 data and utilities
from f1_data import (
    F1_TEAMS, F1_CIRCUITS, RACE_WEEKEND_SESSIONS, SessionType,
    get_realistic_session_result, get_circuit_specific_challenges,
    get_teammate_name, SessionResult
)

# Import NLP and ML libraries
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available. Install with: pip install nltk")

# LLM Integration libraries
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Requests not available. Install with: pip install requests")


# CLI libraries
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

class MessageType(Enum):
    """Types of messages the agent can generate"""
    POST = "post"
    REPLY = "reply"
    STATUS_UPDATE = "status_update"
    MENTION = "mention"
    REACTION = "reaction"

class ContextState(Enum):
    """Current context state of the agent"""
    PRE_WEEKEND = "pre_weekend"
    PRACTICE = "practice"
    QUALIFYING = "qualifying"
    RACE_DAY = "race_day"
    POST_RACE = "post_race"
    OFF_SEASON = "off_season"

@dataclass
class AgentContext:
    """Context information for the F1 agent"""
    driver_name: str
    team: str
    current_circuit: str
    current_session: Optional[SessionType] = None
    current_state: ContextState = ContextState.PRE_WEEKEND
    last_result: Optional[SessionResult] = None
    mood: str = "neutral"
    recent_incidents: List[str] = None
    championship_position: int = 10
    team_mate_name: str = ""
    weekend_type: str = "standard_weekend"
    
    def __post_init__(self):
        if self.recent_incidents is None:
            self.recent_incidents = []

@dataclass
class SocialMediaAction:
    """Represents a social media action performed by the agent"""
    action_type: str
    content: str
    timestamp: datetime
    target: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class F1TextGenerator:
    """Handles text generation using various methods including LLM"""
    
    def __init__(self):
        self.sentiment_analyzer = None
        self.initialize_nltk()
        
    def initialize_nltk(self):
        """Initialize NLTK components"""
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('vader_lexicon')
                nltk.data.find('punkt')
                nltk.data.find('stopwords')
                self.sentiment_analyzer = SentimentIntensityAnalyzer()
            except LookupError:
                print("Downloading required NLTK data...")
                nltk.download('vader_lexicon', quiet=True)
                nltk.download('punkt', quiet=True) 
                nltk.download('stopwords', quiet=True)
                self.sentiment_analyzer = SentimentIntensityAnalyzer()
    
    def generate_with_llm(self, prompt: str, max_tokens: int = 150) -> str:
        """Generate text using Mistral API"""
        api_key = os.getenv('MISTRAL_API_KEY')
        if not api_key or not REQUESTS_AVAILABLE:
            return self.generate_with_templates(prompt)
            
        try:
            url = os.getenv('MISTRAL_BASE_URL', 'https://api.mistral.ai/v1') + '/chat/completions'
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': os.getenv('MISTRAL_MODEL', 'mistral-large-latest'),
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 100,  # Reduced for faster response
                'temperature': 0.7,  # Slightly less random for speed
                'top_p': 0.8
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            raw_content = result['choices'][0]['message']['content'].strip()
            
            # Clean up the response - extract only the actual message
            return self._clean_llm_response(raw_content)
            
        except Exception as e:
            if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
                print(f"Mistral API failed: {e}")
            return self.generate_with_templates(prompt)
    
    def generate_with_templates(self, context_prompt: str) -> str:
        """Fallback text generation using templates and F1 data"""
        # Extract key information from prompt
        session_type = self._extract_session_from_prompt(context_prompt)
        
        # Generate based on extracted context
        if "victory" in context_prompt.lower() or "win" in context_prompt.lower():
            return self._generate_victory_message()
        elif "podium" in context_prompt.lower():
            return self._generate_podium_message()
        elif "difficult" in context_prompt.lower() or "bad" in context_prompt.lower():
            return self._generate_difficult_message()
        elif session_type in ["practice", "fp1", "fp2", "fp3"]:
            return self._generate_practice_message()
        elif session_type == "qualifying":
            return self._generate_qualifying_message()
        else:
            return self._generate_generic_message()
    
    def _clean_llm_response(self, raw_content: str) -> str:
        """Clean LLM response to extract only the actual message content"""
        lines = raw_content.split('\n')
        message_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip meta-information lines
            if (line.startswith('*') and 'chars' in line) or \
               line.startswith('**Why this works:') or \
               line.startswith('- **') or \
               line.startswith('- ') or \
               line.startswith('**') or \
               'F1 terminology' in line or \
               'Emotion:' in line or \
               'Relevant details:' in line:
                continue
            
            # Keep actual message content
            if line and not line.startswith('#') and not line.startswith('Note:'):
                message_lines.append(line)
        
        # Join the cleaned lines and return the first substantial message
        cleaned_message = '\n'.join(message_lines).strip()
        
        # If we have multiple paragraphs, take the first one (likely the actual message)
        paragraphs = cleaned_message.split('\n\n')
        if paragraphs:
            return paragraphs[0].strip()
        
        return cleaned_message or "Ready to give it everything on track! 🏎️ #F1"
    
    def _extract_mood_from_prompt(self, prompt: str) -> str:
        """Extract emotional context from prompt"""
        positive_words = ["win", "victory", "great", "amazing", "fantastic", "perfect"]
        negative_words = ["difficult", "tough", "disappointed", "frustrated", "problems"]
        
        prompt_lower = prompt.lower()
        if any(word in prompt_lower for word in positive_words):
            return "positive"
        elif any(word in prompt_lower for word in negative_words):
            return "negative"
        return "neutral"
    
    def _extract_session_from_prompt(self, prompt: str) -> str:
        """Extract session type from prompt"""
        prompt_lower = prompt.lower()
        if any(term in prompt_lower for term in ["fp1", "fp2", "fp3", "practice"]):
            return "practice"
        elif "qualifying" in prompt_lower:
            return "qualifying"
        elif "race" in prompt_lower:
            return "race"
        return "unknown"
    
    def _generate_victory_message(self) -> str:
        """Generate victory celebration message"""
        templates = [
            "YES! What a race! Huge thanks to the team for the amazing car. We pushed hard and it paid off. #Winner #TeamWork",
            "INCREDIBLE! P1! This feeling never gets old. Massive effort from everyone in the garage. #Victory",
            "Perfect race! The car was amazing today and the strategy was spot on. Thank you to all the fans! #P1",
        ]
        return random.choice(templates)
    
    def _generate_podium_message(self) -> str:
        """Generate podium celebration message"""
        templates = [
            "On the podium! Great team work and solid execution today. Building momentum for the next one! #Podium",
            "P2/P3 feels amazing! Good points for the team and we're moving in the right direction. #Progress",
            "Solid result today! The car felt good and we maximized our potential. Onwards! #TeamWork",
        ]
        return random.choice(templates)
    
    def _generate_difficult_message(self) -> str:
        """Generate message for difficult sessions"""
        templates = [
            "Not the result we wanted today. Gave it my all out there, but things didn't go our way. We'll analyze and come back stronger. #NeverGiveUp",
            "Tough day at the office. These setbacks make us stronger. Time to regroup and focus on the next one. #Resilience",
            "Disappointing result but that's motor racing. The team did everything they could. We'll bounce back! #TeamSpirit",
        ]
        return random.choice(templates)
    
    def _generate_practice_message(self) -> str:
        """Generate practice session message"""
        templates = [
            "Getting some good laps in during practice. Feeling comfortable with the car setup. Let's keep pushing! #Practice",
            "Solid running in the session today. Learning the track and finding the limit. Ready for tomorrow! #Freepractice",
            "Good data collection during practice. The car balance is coming together nicely. #Preparation",
        ]
        return random.choice(templates)
    
    def _generate_qualifying_message(self) -> str:
        """Generate qualifying message"""
        templates = [
            "Qualifying done! Every tenth counts out there. Gave it everything in that final sector. #Quali",
            "That's qualifying in the books. Tight margins today but we're in a good position. #GridPosition",
            "Qualifying session complete. The car felt good in Q3. Looking forward to tomorrow's race! #Qualifying",
        ]
        return random.choice(templates)
    
    def _generate_generic_message(self) -> str:
        """Generate generic F1-style message"""
        templates = [
            "Focus and determination. That's what it takes out there. Ready for the challenge! #F1Life",
            "Another day, another opportunity to push the limits. Grateful for this journey! #Racing",
            "The track is calling. Time to give everything we've got! #NeverSettle",
        ]
        return random.choice(templates)

class F1Agent:
    """
    Main F1 Racer AI Agent class
    
    Capabilities:
    1. Speak (Generate Text): Generate authentic F1 racer messages
    2. Act (Perform Actions): Simulate social media interactions
    3. Think (Contextual Awareness): Maintain and update context state
    """
    
    def __init__(self, driver_name: str = "Alex Driver", team_key: str = "mclaren"):
        """Initialize the F1 Agent with driver and team information"""
        self.context = self._initialize_context(driver_name, team_key)
        self.text_generator = F1TextGenerator()
        self.action_history: List[SocialMediaAction] = []
        self.conversation_memory: List[Dict[str, str]] = []
        
    def _initialize_context(self, driver_name: str, team_key: str) -> AgentContext:
        """Initialize agent context with F1 data"""
        team = F1_TEAMS.get(team_key, F1_TEAMS["mclaren"])
        teammate = get_teammate_name(driver_name)
        
        return AgentContext(
            driver_name=driver_name,
            team=team.name,
            current_circuit="silverstone",  # Default circuit
            team_mate_name=teammate or team.drivers[0] if team.drivers else "Teammate",
            championship_position=random.randint(1, 20)
        )
    
    # =================
    # SPEAK CAPABILITY
    # =================
    
    def speak(self, message_type: MessageType = MessageType.POST, 
             custom_prompt: Optional[str] = None) -> str:
        """
        Generate text message in F1 racer style
        
        Args:
            message_type: Type of message to generate
            custom_prompt: Optional custom context for generation
            
        Returns:
            Generated message string
        """
        prompt = self._build_context_prompt(message_type, custom_prompt)
        
        # Try LLM first, then fall back to templates
        message = self.text_generator.generate_with_llm(prompt)
        
        # Enhance message with F1 context
        enhanced_message = self._enhance_message_with_context(message)
        
        # Store in conversation memory
        self.conversation_memory.append({
            "type": "agent_message",
            "content": enhanced_message,
            "timestamp": datetime.now().isoformat(),
            "context": asdict(self.context)
        })
        
        return enhanced_message
    
    def _build_context_prompt(self, message_type: MessageType, 
                            custom_prompt: Optional[str] = None) -> str:
        """Build context-aware prompt for text generation"""
        circuit_info = F1_CIRCUITS.get(self.context.current_circuit, F1_CIRCUITS["silverstone"])
        
        base_context = f"""
You are {self.context.driver_name}, a Formula 1 driver for {self.context.team}.
Current circuit: {circuit_info.name} ({circuit_info.country})
Current session: {self.context.current_session.value if self.context.current_session else 'between sessions'}
Mood: {self.context.mood}
Championship position: P{self.context.championship_position}
Team mate: {self.context.team_mate_name}

Generate ONLY the social media message. Do not include any explanations, metadata, formatting, or additional text. Just return the raw message content that would be posted on social media.

Requirements:
- Use F1 terminology and racing language
- Show appropriate emotion for the context
- Mention relevant racing details
- Include appropriate hashtags
- Keep under 280 characters
- Return ONLY the message, nothing else

Context details:
- Recent incidents: {', '.join(self.context.recent_incidents) if self.context.recent_incidents else 'None'}
- Circuit characteristics: {', '.join(circuit_info.characteristics)}
"""
        
        if custom_prompt:
            base_context += f"\nSpecific context: {custom_prompt}"
            
        if self.context.last_result:
            base_context += f"\nLast session result: P{self.context.last_result.position}, {self.context.last_result.best_time}"
        
        return base_context
    
    def _enhance_message_with_context(self, message: str) -> str:
        """Enhance generated message with F1-specific context"""
        circuit = F1_CIRCUITS.get(self.context.current_circuit, F1_CIRCUITS["silverstone"])
        
        # Add circuit hashtag if not present
        circuit_tag = f"#{circuit.name.replace(' ', '').replace('-', '')}"
        if circuit_tag not in message and len(message) < 250:
            message += f" {circuit_tag}"
        
        # Add session hashtag if relevant
        if self.context.current_session and len(message) < 250:
            session_tag = f"#{self.context.current_session.value.upper()}"
            if session_tag not in message:
                message += f" {session_tag}"
        
        return message
    
    # ================
    # ACT CAPABILITY
    # ================
    
    def act_post_status(self, content: Optional[str] = None) -> SocialMediaAction:
        """Simulate posting a status update"""
        if not content:
            content = self.speak(MessageType.STATUS_UPDATE)
        
        action = SocialMediaAction(
            action_type="post",
            content=content,
            timestamp=datetime.now(),
            metadata={
                "engagement": random.randint(100, 10000),
                "platform": "social_media"
            }
        )
        
        self.action_history.append(action)
        return action
    
    def act_reply_to_comment(self, original_comment: str) -> SocialMediaAction:
        """Simulate replying to a fan comment"""
        # Analyze sentiment of the comment
        sentiment = "positive"  # Default
        if NLTK_AVAILABLE and self.text_generator.sentiment_analyzer:
            scores = self.text_generator.sentiment_analyzer.polarity_scores(original_comment)
            if scores['compound'] >= 0.05:
                sentiment = "positive"
            elif scores['compound'] <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        # Generate contextual reply
        reply_prompt = f"""
        A fan commented: "{original_comment}"
        The sentiment is {sentiment}.
        Generate a brief, authentic reply that:
        1. Acknowledges the fan
        2. Shows appreciation for support
        3. Stays positive and professional
        4. Uses F1 driver personality
        5. Keeps under 150 characters
        """
        
        reply_content = self.speak(MessageType.REPLY, reply_prompt)
        
        action = SocialMediaAction(
            action_type="reply",
            content=reply_content,
            timestamp=datetime.now(),
            target=original_comment,
            metadata={
                "original_sentiment": sentiment,
                "reply_type": "fan_interaction"
            }
        )
        
        self.action_history.append(action)
        return action
    
    def act_like_post(self, post_content: str) -> SocialMediaAction:
        """Simulate liking a post"""
        action = SocialMediaAction(
            action_type="like",
            content=f"Liked post: {post_content[:100]}...",
            timestamp=datetime.now(),
            target=post_content,
            metadata={
                "interaction_type": "engagement"
            }
        )
        
        self.action_history.append(action)
        return action
    
    def act_mention_someone(self, person_name: str, context: str = "general") -> SocialMediaAction:
        """Simulate mentioning someone in a post"""
        mention_prompt = f"""
        Create a social media post mentioning {person_name}.
        Context: {context}
        Make it authentic, professional, and F1-related.
        Include the mention naturally in the message.
        """
        
        mention_content = self.speak(MessageType.MENTION, mention_prompt)
        
        # Ensure mention is included
        if f"@{person_name}" not in mention_content and person_name not in mention_content:
            mention_content = f"@{person_name} {mention_content}"
        
        action = SocialMediaAction(
            action_type="mention",
            content=mention_content,
            timestamp=datetime.now(),
            target=person_name,
            metadata={
                "mention_context": context,
                "mentioned_person": person_name
            }
        )
        
        self.action_history.append(action)
        return action
    
    # =================
    # THINK CAPABILITY
    # =================
    
    def think_show_context(self) -> Dict[str, Any]:
        """Display current agent context and state"""
        circuit = F1_CIRCUITS.get(self.context.current_circuit, F1_CIRCUITS["silverstone"])
        
        context_info = {
            "driver_info": {
                "name": self.context.driver_name,
                "team": self.context.team,
                "teammate": self.context.team_mate_name,
                "championship_position": f"P{self.context.championship_position}"
            },
            "current_situation": {
                "circuit": f"{circuit.name} ({circuit.country})",
                "session": self.context.current_session.value if self.context.current_session else "None",
                "state": self.context.current_state.value,
                "mood": self.context.mood,
                "weekend_type": self.context.weekend_type
            },
            "recent_activity": {
                "last_result": asdict(self.context.last_result) if self.context.last_result else None,
                "recent_incidents": self.context.recent_incidents,
                "actions_performed": len(self.action_history),
                "last_action": self.action_history[-1].action_type if self.action_history else None
            },
            "circuit_details": {
                "length": f"{circuit.length_km}km",
                "corners": circuit.corners,
                "characteristics": circuit.characteristics,
                "difficulty": circuit.difficulty
            }
        }
        
        return context_info
    
    def think_update_context(self, **kwargs) -> bool:
        """Update agent context with new information"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.context, key):
                    setattr(self.context, key, value)
                    
            # Auto-update related context
            if 'current_circuit' in kwargs:
                circuit = F1_CIRCUITS.get(kwargs['current_circuit'])
                if circuit:
                    challenges = get_circuit_specific_challenges(kwargs['current_circuit'])
                    self.context.recent_incidents = challenges[:2]  # Add circuit challenges
                    
            return True
        except Exception as e:
            print(f"Error updating context: {e}")
            return False
    
    def think_analyze_performance(self) -> Dict[str, Any]:
        """Analyze recent performance and suggest adjustments"""
        analysis = {
            "performance_trend": "stable",
            "key_strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Analyze recent results
        if self.context.last_result:
            if self.context.last_result.position <= 3:
                analysis["performance_trend"] = "excellent"
                analysis["key_strengths"].append("strong pace")
            elif self.context.last_result.position <= 10:
                analysis["performance_trend"] = "good"
                analysis["key_strengths"].append("consistent points scoring")
            else:
                analysis["performance_trend"] = "challenging"
                analysis["areas_for_improvement"].append("qualifying performance")
        
        # Circuit-specific analysis
        circuit = F1_CIRCUITS.get(self.context.current_circuit)
        if circuit:
            if "technical" in circuit.characteristics:
                analysis["recommendations"].append("Focus on setup optimization")
            if "high-speed" in circuit.characteristics:
                analysis["recommendations"].append("Maximize straight-line speed")
            if "street-circuit" in circuit.characteristics:
                analysis["recommendations"].append("Practice precision in tight sections")
        
        return analysis
    
    def run_race_weekend_simulation(self, circuit_key: str = None, 
                                  weekend_type: str = "standard_weekend") -> Dict[str, Any]:
        """Simulate a complete race weekend with context updates"""
        if circuit_key:
            self.think_update_context(current_circuit=circuit_key)
        
        circuit = F1_CIRCUITS.get(self.context.current_circuit, F1_CIRCUITS["silverstone"])
        weekend_sessions = RACE_WEEKEND_SESSIONS[weekend_type]
        
        simulation_results = {
            "circuit": circuit.name,
            "weekend_type": weekend_type,
            "sessions": [],
            "generated_messages": [],
            "final_status": ""
        }
        
        # Simulate each session
        for session_info in weekend_sessions:
            session_type = session_info["session"]
            
            # Update context for session
            self.think_update_context(
                current_session=session_type,
                current_state=self._map_session_to_state(session_type)
            )
            
            # Generate realistic result
            team_performance = self._determine_team_performance()
            result = get_realistic_session_result(session_type, team_performance)
            self.context.last_result = result
            
            # Update mood based on result
            self._update_mood_from_result(result, session_type)
            
            # Generate message for session
            session_message = self.speak(MessageType.POST)
            
            session_data = {
                "session": session_type.value,
                "day": session_info["day"],
                "result": asdict(result),
                "message": session_message
            }
            
            simulation_results["sessions"].append(session_data)
            simulation_results["generated_messages"].append(session_message)
        
        # Generate final weekend summary
        final_result = simulation_results["sessions"][-1]["result"]  # Race result
        self.think_update_context(current_state=ContextState.POST_RACE)
        
        if final_result["position"] <= 3:
            final_status = f"Fantastic weekend! P{final_result['position']} finish! 🏆"
        elif final_result["position"] <= 10:
            final_status = f"Solid points finish in P{final_result['position']}. Good team effort!"
        else:
            final_status = f"Tough weekend, P{final_result['position']}. We'll bounce back stronger!"
        
        simulation_results["final_status"] = final_status
        
        return simulation_results
    
    def _map_session_to_state(self, session_type: SessionType) -> ContextState:
        """Map session type to context state"""
        session_state_map = {
            SessionType.FP1: ContextState.PRACTICE,
            SessionType.FP2: ContextState.PRACTICE,
            SessionType.FP3: ContextState.PRACTICE,
            SessionType.SPRINT_SHOOTOUT: ContextState.QUALIFYING,
            SessionType.SPRINT_RACE: ContextState.RACE_DAY,
            SessionType.QUALIFYING: ContextState.QUALIFYING,
            SessionType.RACE: ContextState.RACE_DAY
        }
        return session_state_map.get(session_type, ContextState.PRE_WEEKEND)
    
    def _determine_team_performance(self) -> str:
        """Determine team performance category based on context"""
        # This could be enhanced with more sophisticated logic
        team_performance_map = {
            "Red Bull Racing": "top_team",
            "Scuderia Ferrari": "top_team", 
            "Mercedes-AMG Petronas F1 Team": "top_team",
            "McLaren F1 Team": "midfield",
            "Aston Martin Aramco Cognizant F1 Team": "midfield",
            "BWT Alpine F1 Team": "midfield",
            "Williams Racing": "midfield",
            "Racing Bulls": "backmarker",
            "MoneyGram Haas F1 Team": "backmarker"
        }
        
        return team_performance_map.get(self.context.team, "midfield")
    
    def _update_mood_from_result(self, result: SessionResult, session_type: SessionType):
        """Update agent mood based on session result"""
        if result.position <= 3:
            self.context.mood = "ecstatic"
        elif result.position <= 6:
            self.context.mood = "satisfied"
        elif result.position <= 10:
            self.context.mood = "neutral"
        elif result.position <= 15:
            self.context.mood = "disappointed"
        else:
            self.context.mood = "frustrated"
            
        # Add incidents to context if any
        if result.incidents:
            self.context.recent_incidents.extend(result.incidents[-2:])  # Keep last 2
    
    # ====================
    # UTILITY METHODS
    # ====================
    
    def get_action_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent action history"""
        recent_actions = self.action_history[-limit:] if limit else self.action_history
        return [asdict(action) for action in recent_actions]
    
    def get_conversation_memory(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent conversation memory"""
        return self.conversation_memory[-limit:] if limit else self.conversation_memory
    
    def reset_context(self, keep_driver_info: bool = True):
        """Reset agent context to default state"""
        driver_name = self.context.driver_name if keep_driver_info else "Alex Driver"
        team_key = next((key for key, team in F1_TEAMS.items() 
                        if team.name == self.context.team), "mclaren")
        
        self.context = self._initialize_context(driver_name, team_key)
        self.action_history.clear()
        self.conversation_memory.clear()
    
    def export_session_data(self) -> Dict[str, Any]:
        """Export current session data for analysis"""
        return {
            "context": asdict(self.context),
            "action_history": self.get_action_history(),
            "conversation_memory": self.get_conversation_memory(),
            "export_timestamp": datetime.now().isoformat()
        }

# Utility function for external usage
def create_f1_agent(driver_name: str, team_key: str) -> F1Agent:
    """Factory function to create F1Agent with validation"""
    if team_key not in F1_TEAMS:
        available_teams = list(F1_TEAMS.keys())
        raise ValueError(f"Invalid team_key '{team_key}'. Available teams: {available_teams}")
    
    return F1Agent(driver_name=driver_name, team_key=team_key)

# ==============================================
# COMMAND LINE INTERFACE
# ==============================================

class F1AgentCLI:
    """Command Line Interface for the F1 AI Agent"""
    
    def __init__(self):
        self.agent: Optional[F1Agent] = None
        self.configured = False
        
    def display_welcome(self):
        """Display welcome message and setup info"""
        if RICH_AVAILABLE:
            welcome_text = Text("🏎️  F1 Racer AI Agent", style="bold red")
            rprint(Panel(welcome_text, title="Welcome", border_style="blue"))
            rprint("[cyan]An AI agent that mimics Formula 1 racer persona and behavior[/cyan]\n")
        else:
            print("=" * 50)
            print("🏎️  F1 Racer AI Agent")
            print("=" * 50)
            print("An AI agent that mimics Formula 1 racer persona and behavior\n")
    
    def configure_agent(self) -> bool:
        """Configure the agent with driver and team information"""
        if RICH_AVAILABLE:
            rprint("[bold yellow]🔧 Agent Configuration[/bold yellow]\n")
        else:
            print("\n🔧 Agent Configuration")
            print("-" * 25)
        
        # Display available teams
        self.display_available_teams()
        
        # Get user input
        if RICH_AVAILABLE:
            driver_name = Prompt.ask("[green]Enter driver name[/green]", default="Alex Driver")
            team_key = Prompt.ask("[green]Enter team key[/green]", 
                                 choices=list(F1_TEAMS.keys()), 
                                 default="mclaren")
        else:
            driver_name = input("Enter driver name (default: Alex Driver): ").strip() or "Alex Driver"
            print("Available teams:", ", ".join(F1_TEAMS.keys()))
            team_key = input("Enter team key (default: mclaren): ").strip() or "mclaren"
            
            if team_key not in F1_TEAMS:
                print(f"Invalid team key. Using 'mclaren'.")
                team_key = "mclaren"
        
        # Create agent
        try:
            self.agent = create_f1_agent(driver_name, team_key)
            self.configured = True
            
            if RICH_AVAILABLE:
                rprint(f"[green]✅ Agent configured successfully![/green]")
                rprint(f"Driver: [bold]{driver_name}[/bold]")
                rprint(f"Team: [bold]{F1_TEAMS[team_key].name}[/bold]")
            else:
                print(f"✅ Agent configured successfully!")
                print(f"Driver: {driver_name}")
                print(f"Team: {F1_TEAMS[team_key].name}")
            
            # Optional: Set initial circuit
            self.configure_initial_context()
            return True
            
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error creating agent: {e}[/red]")
            else:
                print(f"❌ Error creating agent: {e}")
            return False
    
    def configure_initial_context(self):
        """Configure initial race weekend context"""
        if RICH_AVAILABLE:
            setup_context = Confirm.ask("Would you like to set up initial race weekend context?", default=True)
        else:
            response = input("Would you like to set up initial race weekend context? (y/N): ").strip().lower()
            setup_context = response in ['y', 'yes', '1', 'true']
        
        if setup_context:
            self.display_available_circuits()
            
            if RICH_AVAILABLE:
                circuit_key = Prompt.ask("[green]Select circuit[/green]", 
                                       choices=list(F1_CIRCUITS.keys()), 
                                       default="silverstone")
                weekend_type = Prompt.ask("[green]Weekend type[/green]", 
                                        choices=["standard_weekend", "sprint_weekend"],
                                        default="standard_weekend")
            else:
                print("Available circuits:", ", ".join(list(F1_CIRCUITS.keys())[:10]), "... (and more)")
                circuit_key = input("Select circuit (default: silverstone): ").strip() or "silverstone"
                if circuit_key not in F1_CIRCUITS:
                    circuit_key = "silverstone"
                
                print("Weekend types: standard_weekend, sprint_weekend")
                weekend_type = input("Weekend type (default: standard_weekend): ").strip() or "standard_weekend"
                if weekend_type not in ["standard_weekend", "sprint_weekend"]:
                    weekend_type = "standard_weekend"
            
            # Update agent context
            self.agent.think_update_context(
                current_circuit=circuit_key,
                weekend_type=weekend_type,
                current_state=ContextState.PRE_WEEKEND
            )
            
            circuit = F1_CIRCUITS[circuit_key]
            if RICH_AVAILABLE:
                rprint(f"[green]🏁 Context set to {circuit.name} ({circuit.country})[/green]")
            else:
                print(f"🏁 Context set to {circuit.name} ({circuit.country})")
    
    def display_available_teams(self):
        """Display available F1 teams"""
        if RICH_AVAILABLE:
            table = Table(title="Available F1 Teams (2025 Season)")
            table.add_column("Key", style="cyan")
            table.add_column("Team Name", style="white")
            table.add_column("Drivers", style="yellow")
            table.add_column("Engine", style="green")
            
            for key, team in F1_TEAMS.items():
                table.add_row(key, team.name, ", ".join(team.drivers), team.engine)
            
            console.print(table)
        else:
            print("\nAvailable F1 Teams (2025 Season):")
            print("-" * 60)
            for key, team in F1_TEAMS.items():
                print(f"{key:15} | {team.name:30} | {', '.join(team.drivers)}")
    
    def display_available_circuits(self):
        """Display available F1 circuits"""
        if RICH_AVAILABLE:
            rprint("[bold]Available Circuits (showing first 10):[/bold]")
            for key, circuit in list(F1_CIRCUITS.items())[:10]:
                rprint(f"[cyan]{key}[/cyan]: {circuit.name} ({circuit.country})")
            rprint("[dim]...and more circuits available[/dim]")
        else:
            print("\nAvailable Circuits (showing first 10):")
            for key, circuit in list(F1_CIRCUITS.items())[:10]:
                print(f"{key}: {circuit.name} ({circuit.country})")
            print("...and more circuits available")
    
    def display_main_menu(self):
        """Display the main menu options"""
        if RICH_AVAILABLE:
            menu_text = Text("Agent Capabilities", style="bold cyan")
            menu_panel = Panel(menu_text, border_style="blue")
            rprint(menu_panel)
            
            options = [
                ("1", "Generate Message", "(Speak)", "green"),
                ("2", "Post Status Update", "(Act)", "blue"),
                ("3", "Reply to Fan Comment", "(Act)", "blue"),
                ("4", "Like a Post", "(Act)", "blue"),
                ("5", "Mention Someone", "(Act)", "blue"),
                ("6", "Show Current Context", "(Think)", "magenta"),
                ("7", "Update Context", "(Think)", "magenta"),
                ("8", "Run Race Weekend Simulation", "(Full Simulation)", "yellow"),
                ("9", "Exit", "", "red")
            ]
            
            for num, action, category, color in options:
                rprint(f"[{color}]{num}. {action} {category}[/{color}]")
        else:
            print("\n" + "=" * 40)
            print("--- Agent Capabilities ---")
            print("=" * 40)
            print("1. Generate Message (Speak)")
            print("2. Post Status Update (Act)")
            print("3. Reply to Fan Comment (Act)")
            print("4. Like a Post (Act)")
            print("5. Mention Someone (Act)")
            print("6. Show Current Context (Think)")
            print("7. Update Context (Think)")
            print("8. Run Race Weekend Simulation")
            print("9. Exit")
    
    def handle_generate_message(self):
        """Handle generating a message (Speak capability)"""
        if RICH_AVAILABLE:
            rprint("[bold green]🎤 Generate Message (Speak)[/bold green]\n")
            
            message_types = ["post", "reply", "status_update", "mention"]
            msg_type = Prompt.ask("Message type", choices=message_types, default="post")
            custom_context = Prompt.ask("Additional context (optional)", default="")
        else:
            print("\n🎤 Generate Message (Speak)")
            print("-" * 30)
            print("Message types: post, reply, status_update, mention")
            msg_type = input("Message type (default: post): ").strip() or "post"
            custom_context = input("Additional context (optional): ").strip()
        
        try:
            message_type = MessageType(msg_type)
            context = custom_context if custom_context else None
            
            # Generate message
            message = self.agent.speak(message_type, context)
            
            if RICH_AVAILABLE:
                message_panel = Panel(f"[white]{message}[/white]", 
                                    title="Generated Message", 
                                    border_style="green")
                rprint(message_panel)
            else:
                print("\n📱 Generated Message:")
                print("-" * 30)
                print(f"'{message}'")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error generating message: {e}[/red]")
            else:
                print(f"❌ Error generating message: {e}")
    
    def handle_post_status(self):
        """Handle posting status update (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]📱 Post Status Update (Act)[/bold blue]\n")
            custom_content = Prompt.ask("Custom content (leave empty to auto-generate)", default="")
        else:
            print("\n📱 Post Status Update (Act)")
            print("-" * 30)
            custom_content = input("Custom content (leave empty to auto-generate): ").strip()
        
        try:
            content = custom_content if custom_content else None
            action = self.agent.act_post_status(content)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Status posted successfully![/green]")
                post_panel = Panel(f"[white]{action.content}[/white]", 
                                 title="Posted Content", 
                                 border_style="blue")
                rprint(post_panel)
                rprint(f"[dim]Engagement: {action.metadata.get('engagement', 'N/A')} interactions[/dim]")
            else:
                print("✅ Status posted successfully!")
                print(f"Content: '{action.content}'")
                print(f"Engagement: {action.metadata.get('engagement', 'N/A')} interactions")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error posting status: {e}[/red]")
            else:
                print(f"❌ Error posting status: {e}")
    
    def handle_reply_comment(self):
        """Handle replying to fan comment (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]💬 Reply to Fan Comment (Act)[/bold blue]\n")
            fan_comment = Prompt.ask("Enter the fan comment to reply to")
        else:
            print("\n💬 Reply to Fan Comment (Act)")
            print("-" * 30)
            fan_comment = input("Enter the fan comment to reply to: ").strip()
        
        if not fan_comment:
            if RICH_AVAILABLE:
                rprint("[yellow]⚠️  No comment provided[/yellow]")
            else:
                print("⚠️  No comment provided")
            return
        
        try:
            action = self.agent.act_reply_to_comment(fan_comment)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Reply posted successfully![/green]")
                rprint(f"[dim]Original comment:[/dim] [italic]{fan_comment}[/italic]")
                reply_panel = Panel(f"[white]{action.content}[/white]", 
                                  title="Your Reply", 
                                  border_style="blue")
                rprint(reply_panel)
                rprint(f"[dim]Detected sentiment: {action.metadata.get('original_sentiment', 'unknown')}[/dim]")
            else:
                print("✅ Reply posted successfully!")
                print(f"Original: '{fan_comment}'")
                print(f"Reply: '{action.content}'")
                print(f"Sentiment: {action.metadata.get('original_sentiment', 'unknown')}")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error posting reply: {e}[/red]")
            else:
                print(f"❌ Error posting reply: {e}")
    
    def handle_like_post(self):
        """Handle liking a post (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]👍 Like a Post (Act)[/bold blue]\n")
            post_content = Prompt.ask("Enter the post content to like")
        else:
            print("\n👍 Like a Post (Act)")
            print("-" * 30)
            post_content = input("Enter the post content to like: ").strip()
        
        if not post_content:
            if RICH_AVAILABLE:
                rprint("[yellow]⚠️  No post content provided[/yellow]")
            else:
                print("⚠️  No post content provided")
            return
        
        try:
            self.agent.act_like_post(post_content)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Post liked successfully![/green]")
                rprint(f"[dim]Liked post:[/dim] [italic]{post_content[:100]}{'...' if len(post_content) > 100 else ''}[/italic]")
            else:
                print("✅ Post liked successfully!")
                print(f"Liked: '{post_content[:100]}{'...' if len(post_content) > 100 else ''}'")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error liking post: {e}[/red]")
            else:
                print(f"❌ Error liking post: {e}")
    
    def handle_mention_someone(self):
        """Handle mentioning someone (Act capability)"""
        if RICH_AVAILABLE:
            rprint("[bold blue]@️ Mention Someone (Act)[/bold blue]\n")
            person_name = Prompt.ask("Enter person name to mention")
            context = Prompt.ask("Mention context", default="general")
        else:
            print("\n@️ Mention Someone (Act)")
            print("-" * 30)
            person_name = input("Enter person name to mention: ").strip()
            context = input("Mention context (default: general): ").strip() or "general"
        
        if not person_name:
            if RICH_AVAILABLE:
                rprint("[yellow]⚠️  No person name provided[/yellow]")
            else:
                print("⚠️  No person name provided")
            return
        
        try:
            action = self.agent.act_mention_someone(person_name, context)
            
            if RICH_AVAILABLE:
                rprint("[green]✅ Mention posted successfully![/green]")
                mention_panel = Panel(f"[white]{action.content}[/white]", 
                                    title=f"Mentioning @{person_name}", 
                                    border_style="blue")
                rprint(mention_panel)
                rprint(f"[dim]Context: {action.metadata.get('mention_context', 'general')}[/dim]")
            else:
                print("✅ Mention posted successfully!")
                print(f"Content: '{action.content}'")
                print(f"Context: {action.metadata.get('mention_context', 'general')}")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error posting mention: {e}[/red]")
            else:
                print(f"❌ Error posting mention: {e}")
    
    def handle_show_context(self):
        """Handle showing current context (Think capability)"""
        if RICH_AVAILABLE:
            rprint("[bold magenta]🧠 Show Current Context (Think)[/bold magenta]\n")
        else:
            print("\n🧠 Show Current Context (Think)")
            print("-" * 35)
        
        try:
            context = self.agent.think_show_context()
            
            if RICH_AVAILABLE:
                # Driver info
                driver_table = Table(title="Driver Information")
                driver_table.add_column("Property", style="cyan")
                driver_table.add_column("Value", style="white")
                
                for key, value in context["driver_info"].items():
                    driver_table.add_row(key.replace("_", " ").title(), str(value))
                
                console.print(driver_table)
                
                # Current situation
                situation_table = Table(title="Current Situation")
                situation_table.add_column("Property", style="cyan")
                situation_table.add_column("Value", style="white")
                
                for key, value in context["current_situation"].items():
                    situation_table.add_row(key.replace("_", " ").title(), str(value))
                
                console.print(situation_table)
                
                # Recent activity
                if context["recent_activity"]["last_result"]:
                    result = context["recent_activity"]["last_result"]
                    rprint(f"[yellow]Last Result:[/yellow] P{result['position']} - {result['best_time']} ({result['laps_completed']} laps)")
                
                if context["recent_activity"]["recent_incidents"]:
                    rprint(f"[red]Recent Incidents:[/red] {', '.join(context['recent_activity']['recent_incidents'])}")
                    
            else:
                print("Driver Information:")
                for key, value in context["driver_info"].items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
                
                print("\nCurrent Situation:")
                for key, value in context["current_situation"].items():
                    print(f"  {key.replace('_', ' ').title()}: {value}")
                
                print("\nRecent Activity:")
                for key, value in context["recent_activity"].items():
                    if value:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
                        
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error showing context: {e}[/red]")
            else:
                print(f"❌ Error showing context: {e}")
    
    def handle_update_context(self):
        """Handle updating context (Think capability)"""
        if RICH_AVAILABLE:
            rprint("[bold magenta]🔄 Update Context (Think)[/bold magenta]\n")
            
            # Show current context first
            current_context = self.agent.think_show_context()
            rprint(f"[dim]Current circuit: {current_context['current_situation']['circuit']}[/dim]")
            rprint(f"[dim]Current session: {current_context['current_situation']['session']}[/dim]")
            rprint(f"[dim]Current mood: {current_context['current_situation']['mood']}[/dim]\n")
            
            # Get updates
            new_circuit = Prompt.ask("New circuit", 
                                   choices=list(F1_CIRCUITS.keys()) + [""], 
                                   default="")
            
            new_session = Prompt.ask("New session", 
                                   choices=[s.value for s in SessionType] + [""], 
                                   default="")
            
            new_mood = Prompt.ask("New mood", 
                                choices=["ecstatic", "satisfied", "neutral", "disappointed", "frustrated", ""], 
                                default="")
        else:
            print("\n🔄 Update Context (Think)")
            print("-" * 30)
            
            # Show current values
            current_context = self.agent.think_show_context()
            print(f"Current circuit: {current_context['current_situation']['circuit']}")
            print(f"Current session: {current_context['current_situation']['session']}")
            print(f"Current mood: {current_context['current_situation']['mood']}")
            
            print("\nEnter new values (leave empty to keep current):")
            print("Available circuits:", ", ".join(list(F1_CIRCUITS.keys())[:5]), "... (and more)")
            new_circuit = input("New circuit: ").strip()
            
            print("Sessions: fp1, fp2, fp3, sprint_shootout, sprint_race, qualifying, race")
            new_session = input("New session: ").strip()
            
            print("Moods: ecstatic, satisfied, neutral, disappointed, frustrated")
            new_mood = input("New mood: ").strip()
        
        # Apply updates
        updates = {}
        if new_circuit and new_circuit in F1_CIRCUITS:
            updates["current_circuit"] = new_circuit
        if new_session:
            try:
                updates["current_session"] = SessionType(new_session)
            except ValueError:
                if RICH_AVAILABLE:
                    rprint(f"[yellow]⚠️  Invalid session type: {new_session}[/yellow]")
                else:
                    print(f"⚠️  Invalid session type: {new_session}")
        if new_mood:
            updates["mood"] = new_mood
        
        if updates:
            success = self.agent.think_update_context(**updates)
            if success:
                if RICH_AVAILABLE:
                    rprint("[green]✅ Context updated successfully![/green]")
                else:
                    print("✅ Context updated successfully!")
            else:
                if RICH_AVAILABLE:
                    rprint("[red]❌ Error updating context[/red]")
                else:
                    print("❌ Error updating context")
        else:
            if RICH_AVAILABLE:
                rprint("[yellow]ℹ️  No updates provided[/yellow]")
            else:
                print("ℹ️  No updates provided")
    
    def handle_race_simulation(self):
        """Handle running race weekend simulation"""
        if RICH_AVAILABLE:
            rprint("[bold yellow]🏁 Run Race Weekend Simulation[/bold yellow]\n")
            
            circuit_key = Prompt.ask("Select circuit for simulation", 
                                   choices=list(F1_CIRCUITS.keys()), 
                                   default=self.agent.context.current_circuit)
            
            weekend_type = Prompt.ask("Weekend type", 
                                    choices=["standard_weekend", "sprint_weekend"], 
                                    default="standard_weekend")
        else:
            print("\n🏁 Run Race Weekend Simulation")
            print("-" * 35)
            
            print("Available circuits:", ", ".join(list(F1_CIRCUITS.keys())[:10]), "... (and more)")
            current_circuit = self.agent.context.current_circuit
            circuit_key = input(f"Select circuit (default: {current_circuit}): ").strip() or current_circuit
            
            print("Weekend types: standard_weekend, sprint_weekend")
            weekend_type = input("Weekend type (default: standard_weekend): ").strip() or "standard_weekend"
        
        if circuit_key not in F1_CIRCUITS:
            circuit_key = self.agent.context.current_circuit
        
        try:
            if RICH_AVAILABLE:
                with console.status("[bold green]Running race weekend simulation...") as status:
                    results = self.agent.run_race_weekend_simulation(circuit_key, weekend_type)
            else:
                print("Running race weekend simulation...")
                results = self.agent.run_race_weekend_simulation(circuit_key, weekend_type)
            
            # Display results
            if RICH_AVAILABLE:
                simulation_panel = Panel(f"[white]{results['circuit']} - {results['weekend_type'].replace('_', ' ').title()}[/white]", 
                                       title="Weekend Simulation Results", 
                                       border_style="yellow")
                rprint(simulation_panel)
                
                # Session results
                for session in results["sessions"]:
                    rprint(f"[cyan]{session['day']} - {session['session'].title()}:[/cyan]")
                    rprint(f"  Position: P{session['result']['position']}")
                    rprint(f"  Best Time: {session['result']['best_time']}")
                    rprint(f"  Message: [italic]{session['message']}[/italic]\n")
                
                final_panel = Panel(f"[white]{results['final_status']}[/white]", 
                                  title="Weekend Summary", 
                                  border_style="green")
                rprint(final_panel)
            else:
                print(f"\n🏁 Weekend Simulation: {results['circuit']} - {results['weekend_type'].replace('_', ' ').title()}")
                print("=" * 60)
                
                for session in results["sessions"]:
                    print(f"\n{session['day']} - {session['session'].title()}:")
                    print(f"  Position: P{session['result']['position']}")
                    print(f"  Best Time: {session['result']['best_time']}")
                    print(f"  Message: '{session['message']}'")
                
                print(f"\n🏆 Weekend Summary: {results['final_status']}")
                
        except Exception as e:
            if RICH_AVAILABLE:
                rprint(f"[red]❌ Error running simulation: {e}[/red]")
            else:
                print(f"❌ Error running simulation: {e}")
    
    def run(self):
        """Main CLI loop"""
        self.display_welcome()
        
        # Configure agent first
        if not self.configure_agent():
            if RICH_AVAILABLE:
                rprint("[red]❌ Agent configuration failed. Exiting.[/red]")
            else:
                print("❌ Agent configuration failed. Exiting.")
            sys.exit(1)
        
        # Main menu loop
        while True:
            try:
                self.display_main_menu()
                
                if RICH_AVAILABLE:
                    choice = Prompt.ask("\n[bold]Select option[/bold]", 
                                      choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
                else:
                    choice = input("\nSelect option (1-9): ").strip()
                
                if choice == "1":
                    self.handle_generate_message()
                elif choice == "2":
                    self.handle_post_status()
                elif choice == "3":
                    self.handle_reply_comment()
                elif choice == "4":
                    self.handle_like_post()
                elif choice == "5":
                    self.handle_mention_someone()
                elif choice == "6":
                    self.handle_show_context()
                elif choice == "7":
                    self.handle_update_context()
                elif choice == "8":
                    self.handle_race_simulation()
                elif choice == "9":
                    if RICH_AVAILABLE:
                        rprint("[yellow]👋 Thanks for using F1 Racer AI Agent![/yellow]")
                    else:
                        print("👋 Thanks for using F1 Racer AI Agent!")
                    break
                else:
                    if RICH_AVAILABLE:
                        rprint("[red]❌ Invalid choice. Please select 1-9.[/red]")
                    else:
                        print("❌ Invalid choice. Please select 1-9.")
                
                # Pause between operations
                if RICH_AVAILABLE:
                    input("\n[dim]Press Enter to continue...[/dim]")
                else:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                if RICH_AVAILABLE:
                    rprint("\n[yellow]👋 Goodbye![/yellow]")
                else:
                    print("\n👋 Goodbye!")
                break
            except Exception as e:
                if RICH_AVAILABLE:
                    rprint(f"[red]❌ Unexpected error: {e}[/red]")
                else:
                    print(f"❌ Unexpected error: {e}")

def main():
    """Entry point for the CLI application"""
    cli = F1AgentCLI()
    cli.run()

if __name__ == "__main__":
    main()