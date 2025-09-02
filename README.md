# 🏎️ F1 Racer AI Agent

An intelligent AI agent that mimics the persona and behavior of a Formula One racer, designed for authentic social media interactions and race weekend simulations.

## 🎯 Agent Capabilities

The F1 Racer AI Agent implements three core capabilities inspired by F1 driver behavior:

### 🎤 **Speak** (Generate Text)
- Generates authentic F1 racer-style messages and social media posts
- Uses F1-specific terminology, emotions, and context
- Adapts language based on race results, circuit characteristics, and current mood
- Integrates with Mistral LLM for advanced text generation with template fallback

### 🎬 **Act** (Perform Actions)
Simulates realistic social media interactions:
- **Post Status Update**: Create race weekend updates and announcements
- **Reply to Fan Comments**: Respond to fan interactions with contextual awareness
- **Like Posts**: Engage with content from other drivers, teams, or fans
- **Mention Someone**: Tag teammates, competitors, or team personnel in posts

### 🧠 **Think** (Contextual Awareness)
- Maintains comprehensive race weekend context (practice, qualifying, race)
- Tracks driver performance, mood, and recent incidents
- Adapts responses based on circuit characteristics and session results
- Manages championship position and team dynamics

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** is required
2. **Mistral API key** from [Mistral AI](https://mistral.ai/)

### Installation

1. Clone or download the repository:
```bash
git clone https://github.com/yourusername/f1_racer_ai_agent.git
cd f1_racer_ai_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Mistral API key
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Running the Agent

#### Interactive CLI Mode
```bash
python3 f1_agent.py
```

The CLI provides an intuitive interface with the following menu:
```
--- Agent Capabilities ---
1. Generate Message (Speak)
2. Post Status Update (Act)
3. Reply to Fan Comment (Act)
4. Like a Post (Act)
5. Mention Someone (Act)
6. Show Current Context (Think)
7. Update Context (Think)
8. Run Race Weekend Simulation
9. Exit
```

#### Web Interface (Recommended)
For a more user-friendly experience, use the professional web interface:

```bash
# Simple start
python3 run_web.py

# Custom port
python3 run_web.py --port 8080

# Debug mode
python3 run_web.py --debug

# Accept external connections
python3 run_web.py --host 0.0.0.0
```

Then open http://localhost:5000 in your browser.

The web interface provides:
- Clean, professional F1-themed design
- All CLI functionality in a dashboard format
- Real-time agent configuration and interaction
- Responsive design for desktop and mobile
- Session-based agent management

#### Python Script Usage
```python
from f1_agent import create_f1_agent
from f1_data import F1_TEAMS

# Create agent
agent = create_f1_agent("Lewis Hamilton", "ferrari")

# Generate a message
message = agent.speak()
print(message)

# Simulate posting a status
action = agent.act_post_status()
print(f"Posted: {action.content}")

# Show current context
context = agent.think_show_context()
print(context)
```

#### Testing Basic Functionality
```bash
python3 test_agent.py
```

## 📱 Example Outputs

### After a Victory
**Context**: P1 finish at Silverstone
```
"YES! What a race! Huge thanks to the team for the amazing car. We pushed hard and it paid off. #Winner #TeamWork #SilverstoneCircuit"
```

### During Practice Session
**Context**: FP2 at Monaco, good session
```
"Getting some good laps in during FP2. Feeling comfortable with the car setup. Let's keep pushing! #FP2 #CircuitDeMonaco #Practice"
```

### After a Difficult Race
**Context**: P15 finish due to mechanical issues
```
"Not the result we wanted today. Gave it my all out there, but things didn't go our way. We'll analyze and come back stronger. #NeverGiveUp #TeamSpirit"
```

### Replying to Fan Comment
**Fan**: "Great drive today, Lewis!"
**Agent Reply**: 
```
"Thanks for the support! Every cheer makes a difference. The fans are incredible here! 🙌"
```

### Race Weekend Simulation Example
```
🏁 Weekend Simulation: Silverstone Circuit - Standard Weekend
============================================================

Friday - FP1:
  Position: P4
  Best Time: 1:24.567
  Message: 'Solid running in FP1. Learning the track surface and finding our baseline setup. #FP1 #SilverstoneCircuit'

Friday - FP2:
  Position: P2
  Best Time: 1:23.234
  Message: 'Great pace in FP2! The car balance is coming together nicely. Team did fantastic work! #FP2 #SilverstoneCircuit'

Saturday - FP3:
  Position: P3
  Best Time: 1:22.890
  Message: 'Final practice done. Good preparation for qualifying. Ready to fight for pole! #FP3 #SilverstoneCircuit'

Saturday - Qualifying:
  Position: P2
  Best Time: 1:21.456
  Message: 'P2 on the grid! Gave everything in Q3. Great team effort to get us there! #Qualifying #SilverstoneCircuit'

Sunday - Race:
  Position: P1
  Best Time: 1:22.123
  Message: 'INCREDIBLE! P1! This feeling never gets old. Massive effort from everyone in the garage. #Victory #SilverstoneCircuit'

🏆 Weekend Summary: Fantastic weekend! P1 finish! 🏆
```

## 🏗️ Architecture & Design Choices

### Hybrid Approach Implementation
The agent uses a sophisticated hybrid approach combining multiple technologies:

**🤖 Language Model Integration**
- **Primary**: Mistral LLM via API for contextual, dynamic text generation
- **Fallback**: Template-based generation using F1-specific patterns and vocabulary
- **Graceful Degradation**: Automatically switches to templates if LLM is unavailable

**📊 NLP Libraries Integration**
- **NLTK**: Sentiment analysis for fan comment responses and mood tracking
- **Pattern Matching**: Context extraction and F1 terminology integration
- **Text Enhancement**: Automatic hashtag and mention generation

### Context Management System
```python
@dataclass
class AgentContext:
    driver_name: str
    team: str
    current_circuit: str
    current_session: Optional[SessionType]
    current_state: ContextState
    last_result: Optional[SessionResult]
    mood: str
    recent_incidents: List[str]
    championship_position: int
```

The context system maintains:
- **Driver Identity**: Name, team affiliation, teammate relationships
- **Race Weekend State**: Current session, circuit, performance results
- **Emotional Context**: Mood based on recent performance and incidents
- **Historical Tracking**: Recent actions, conversation memory, performance trends

### F1 Data Integration
Comprehensive F1 database includes:
- **Teams & Drivers**: 2025 season lineup with accurate team information
- **Circuits**: 24 race calendar with detailed circuit characteristics
- **Technical Terms**: Racing vocabulary and radio phrases
- **Session Structure**: Realistic weekend formats (standard and sprint weekends)

## 🎮 Features

### Advanced Text Generation
- **Context-Aware Prompts**: Builds detailed prompts with circuit info, session data, and emotional state
- **F1 Terminology**: Natural integration of racing terms, team references, and technical language
- **Emotional Adaptation**: Adjusts tone and sentiment based on performance and context
- **Character Limits**: Respects social media constraints (280 characters)

### Realistic Simulations
- **Performance Modeling**: Team-based performance categories (top team, midfield, backmarker)
- **Session Results**: Realistic lap times, positions, and incident generation
- **Circuit-Specific**: Adapts to track characteristics and challenges
- **Weekend Progression**: Maintains continuity across practice, qualifying, and race

### Social Media Interactions
- **Sentiment Analysis**: Analyzes fan comments and generates appropriate responses
- **Engagement Tracking**: Simulates realistic social media metrics
- **Mention Handling**: Natural integration of @ mentions and hashtags
- **Content Variety**: Different message types for various social media scenarios

## 🛠️ Technical Implementation

### File Structure
```
f1_racer_ai_agent/
├── f1_agent.py          # Core agent implementation with CLI
├── f1_data.py           # F1 data and utilities
├── app.py               # Flask web application
├── run_web.py           # Web interface launcher
├── templates/           # HTML templates for web interface
├── static/              # CSS and JavaScript for web interface
├── test_agent.py        # Testing script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (your API key)
├── .env.example         # Environment variables template
└── README.md           # Documentation
```

### Key Classes
- **`F1Agent`**: Main agent with Speak/Act/Think capabilities
- **`F1TextGenerator`**: Handles LLM integration and text generation
- **`AgentContext`**: Maintains race weekend and driver context
- **`F1AgentCLI`**: Interactive command-line interface

### Dependencies
- **Core ML/NLP**: `transformers`, `torch`, `nltk`, `spacy`
- **LLM Integration**: `requests` (for Mistral API)
- **CLI Enhancement**: `rich`, `click`, `colorama`
- **Data Processing**: `numpy`, `pandas`, `python-dateutil`
- **Environment**: `python-dotenv`

## 🎛️ Configuration Options

### Driver & Team Selection
Configure any driver-team combination:
```python
# Available teams (2025 season)
teams = {
    "red_bull": "Red Bull Racing",
    "ferrari": "Scuderia Ferrari", 
    "mercedes": "Mercedes-AMG Petronas F1 Team",
    "mclaren": "McLaren F1 Team",
    "aston_martin": "Aston Martin Aramco Cognizant F1 Team",
    "alpine": "BWT Alpine F1 Team",
    "williams": "Williams Racing",
    "racing_bulls": "Racing Bulls",
    "haas": "MoneyGram Haas F1 Team"
}
```

### Context Customization
```python
# Update agent context
agent.think_update_context(
    current_circuit="monaco",
    current_session=SessionType.QUALIFYING,
    mood="confident",
    championship_position=3
)
```

### Environment Variables
```bash
# Mistral API Configuration
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-large-latest
MISTRAL_BASE_URL=https://api.mistral.ai/v1

# Agent Configuration
DEFAULT_DRIVER=Alex Driver
DEFAULT_TEAM=mclaren
DEFAULT_CIRCUIT=silverstone

# CLI Configuration
ENABLE_RICH_CLI=true
DEBUG_MODE=false
```

## 🏆 Design Philosophy & Challenges

### Design Choices

**1. Mistral API Integration**
- **Rationale**: Provides high-quality, contextual text generation for authentic F1 content
- **Implementation**: Direct API integration with comprehensive error handling
- **Benefits**: Advanced natural language understanding and F1 persona accuracy

**2. Rich Context Management**
- **Challenge**: Maintaining realistic F1 context across interactions
- **Solution**: Comprehensive context dataclass with automatic updates
- **Result**: Authentic responses that adapt to race weekend progression

**3. Modular Architecture**
- **Design**: Separated concerns (agent logic, data, CLI, text generation)
- **Benefits**: Easy testing, maintenance, and extensibility
- **Future-Proof**: Can easily add new capabilities or data sources

**4. CLI-First Approach**
- **Philosophy**: Interactive experience over programmatic usage
- **Implementation**: Rich terminal interface with fallback to basic CLI
- **User Experience**: Intuitive menu system matching the specified structure

### Challenges Encountered

**1. F1 Authenticity**
- **Challenge**: Generating messages that sound authentically F1
- **Solution**: Extensive F1 data integration and context-aware prompts
- **Result**: Messages that include proper terminology, emotions, and references

**2. Context Continuity**
- **Challenge**: Maintaining context across different agent interactions
- **Solution**: Persistent context state with automatic updates
- **Result**: Coherent personality that remembers recent events and adapts accordingly

**3. API Reliability**
- **Challenge**: Mistral API availability and response consistency
- **Solution**: Template-based fallback system with graceful degradation
- **Result**: Consistent user experience regardless of API status

**4. Social Media Simulation**
- **Challenge**: Realistic social media interaction patterns
- **Solution**: Sentiment analysis, engagement metrics, and contextual responses
- **Result**: Believable social media behavior simulation

## 🔮 Future Enhancements

- **Multi-Language Support**: Generate content in multiple languages for international F1 audience
- **Historical Data Integration**: Include past race results and career statistics
- **Advanced Sentiment Analysis**: More sophisticated emotion detection and response
- **Real-Time F1 Data**: Integration with live F1 timing and results
- **Voice Generation**: Text-to-speech for more immersive interactions
- **Image Generation**: Create race-related visual content

## 📜 License & Usage

This project is created for educational and assessment purposes. The F1 data is based on publicly available information and is used for simulation purposes only.

## 🤝 Contributing

This is an assessment project, but suggestions and improvements are welcome through issues and pull requests.

---

**🏁 Ready to race? Start your engines with `python3 f1_agent.py`!**