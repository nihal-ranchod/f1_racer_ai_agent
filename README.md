# F1 Racer AI Agent

An intelligent Formula 1 driver persona that simulates authentic F1 driver behaviour across social media interactions and race weekend scenarios. The agent combines real F1 data, natural language processing, and contextual awareness to generate realistic driver responses, social media posts, and race weekend narratives.

## Agent Capabilities

The F1 Racer AI Agent features three core capabilities inspired by authentic F1 driver behaviour:

### **SPEAK** - Message Generation
- Generate authentic F1-style social media posts and messages
- Context-aware responses based on race weekend phase, circuit, and performance
- Multiple message types: posts, replies, status updates, mentions
- Integration with LLM (Mistral API) for enhanced text generation with template fallback

### **ACT** - Social Media Actions
- **Post Status Updates**: Share race weekend updates and general content
- **Reply to Fan Comments**: Contextual responses with sentiment analysis
- **Like Posts**: Engage with other content
- **Mention Others**: Tag teammates, competitors, or personalities
- Realistic engagement metrics and interaction tracking

### **THINK** - Contextual Awareness
- Dynamic context management throughout race weekends
- Circuit-specific challenges and characteristics
- Mood adaptation based on performance and results
- Championship position and team dynamics awareness
- Complete race weekend simulation with session-by-session progression

## Setup & Installation

### Prerequisites
- Python 3.11 or higher
- Git

### Option 1: CLI Version

1. **Clone and Setup**
```bash
git clone <repository-url>
cd f1_racer_ai_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure Environment (Optional)**
```bash
cp .env.example .env
# Edit .env file to add your Mistral API key for enhanced text generation:
# MISTRAL_API_KEY=your_mistral_api_key_here
```

3. **Run CLI Interface**
```bash
python f1_agent.py
```

### Option 2: Web Application

1. **Complete CLI setup steps above**

2. **Launch Web Interface**
```bash
python run_web.py
# Or with custom settings:
python run_web.py --host 0.0.0.0 --port 8080 --debug
```

3. **Access Web Interface**
   - Open browser to `http://localhost:5000`
   - Follow the web configuration guide below

### Option 3: Docker Container

1. **Using Docker Compose (Recommended)**
```bash
# Clone repository and navigate to directory
git clone <repository-url>
cd f1_racer_ai_agent

# Copy environment file and configure (optional)
cp .env.example .env
# Edit .env to add your Mistral API key

# Build and run
docker-compose up --build
```

2. **Using Docker directly**
```bash
# Build image
docker build -t f1-racer-ai .

# Run container
docker run -p 5000:5000 --env-file .env f1-racer-ai
```

3. **Access the application at `http://localhost:5000`**

## Web Application User Guide

### Step 1: Agent Configuration
When you first access the web interface, you'll see the configuration page:

1. **Driver Name**: Enter your F1 driver name (e.g., "Lewis Hamilton", "Max Verstappen")
2. **Team Selection**: Choose from all current F1 teams:
   - Red Bull Racing, Ferrari, Mercedes, McLaren
   - Aston Martin, Alpine, Williams, Racing Bulls, Haas
3. **Initial Circuit**: Select starting circuit (default: Silverstone)
4. **Weekend Type**: Choose between:
   - **Standard Weekend**: FP1, FP2, FP3, Qualifying, Race
   - **Sprint Weekend**: FP1, Sprint Shootout, Sprint Race, Qualifying, Race

### Step 2: Using the Dashboard

After configuration, you'll access the main dashboard with these sections:

#### **SPEAK - Message Generation**
- **Message Type**: Select post type (post, reply, status_update, mention)
- **Custom Context**: Add specific context (e.g., "after qualifying P3", "celebrating podium finish")
- Generates authentic F1-style messages based on current context

#### **ACT - Social Media Actions**
- **Post Status**: Create social media posts with engagement metrics
- **Reply to Comments**: Respond to fan comments with sentiment analysis
- **Like Posts**: Simulate liking other posts
- **Mention Someone**: Create posts mentioning other drivers or personalities

#### **THINK - Context Management**
- **View Context**: See current driver info, circuit, session, mood, and recent activity
- **Update Context**: Modify:
  - **Circuit**: Change current racing location
  - **Session**: Set current session (fp1, fp2, fp3, qualifying, race)
  - **Mood**: Adjust emotional state (ecstatic, satisfied, neutral, disappointed, frustrated)

#### **Race Weekend Simulation**
- **Circuit Selection**: Choose any F1 circuit for simulation
- **Weekend Type**: Standard or Sprint weekend format
- Runs complete weekend with realistic results and generated messages

### Context Fields Explained

| Field | Description | Impact on Agent |
|-------|-------------|----------------|
| **Driver Name** | The F1 driver being simulated | Affects teammate identification and team context |
| **Team** | Current F1 team | Influences car performance expectations and team culture |
| **Circuit** | Current racing circuit | Determines circuit-specific challenges and characteristics |
| **Session** | Current F1 session type | Affects message tone and content focus |
| **Mood** | Emotional state | Influences message sentiment and response style |
| **Championship Position** | Current standings | Affects confidence level and expectations |
| **Recent Incidents** | Recent racing events | Provides context for current challenges |

## Example Agent Outputs

### After a Victory
```
"Silverstone, you absolute *beauty*—high-speed, flat-out, and that final lap? Pure magic. The team nailed it, the MCL60 was a *rocket* through Maggots & Becketts, and that slipstream duel? *Chef’s kiss.* P6 in the championship? Not for long. 😉 This one’s for the orange army. **LET’S GO!** #LND #ForTheFans #BritishGP 🧡"
```

### After a Difficult Race
```
"Tough one at home today. Silverstone didn’t play to our strengths—struggled with aero efficiency in the high-speed stuff and got caught out in the slipstream battles. Not the points we wanted, but we’ll dig deep. P10 in the championship isn’t where we belong. Thanks for the support—we’ll come  back stronger. 🧡 #Lando #McLaren #BritishGP #NeverGiveUp"
```

### During Practice
```
FP3 done at this absolute beast of a track! 🏎️💨 Silverstone’s high-speed flow is next level—nailed some solid laps but still chasing that last bit of aero balance through Maggots & Beckets. Slipstream battles tomorrow? Bring it. 🇬🇧 #HomeOfF1 #McLaren #P10ButHungry #FP3 
```

### Fan Interaction Example
```
**Fan Comment**: "Great qualifying session! P2 is amazing!"
**Agent Reply**: "Cheers, mate! P2 feels good—especially here at Silverstone. The car’s hooked up, and the crowd’s energy is next level. Let’s keep pushing! 💨🏆#L4NDO #McLaren #BritishGP #SilverstoneCircuit #FP3"
```

## Design Choices & Architecture

### Core Design Principles

1. **Authenticity First**: Every aspect built on real F1 data, terminology, and driver behaviour patterns
2. **Modular Architecture**: Separate modules for agent logic, F1 data, and web interface
3. **Graceful Degradation**: System works even when external dependencies are unavailable
4. **Context-Aware Responses**: Agent behaviour adapts dynamically based on race weekend phase and performance

### Key Technical Decisions

- **Enum-Based State Management**: Used Python enums for session types and context states for type safety
- **Dataclass Integration**: Leveraged dataclasses for clean data structures and JSON serialization
- **Multi-Interface Support**: Both CLI and web interfaces share the same core agent logic
- **Docker-First Deployment**: Optimized for containerized deployment with security best practices

### Data Architecture

- **F1 Teams & Drivers**: Complete 2025 season data with realistic driver lineups
- **Circuit Database**: 24 circuits with authentic characteristics, lap records, and technical details
- **Session Results**: Probabilistic result generation based on team performance tiers
- **Sentiment Analysis**: NLTK VADER sentiment analysis for contextual fan interactions

### Text Generation Strategy

- **Primary**: Mistral LLM API integration for advanced, contextual text generation
- **Fallback**: Template-based generation using F1-specific patterns and vocabulary
- **Context Building**: Detailed prompts incorporating circuit info, session data, and emotional state
- **Response Cleaning**: Automatic filtering of LLM metadata to extract clean social media content

## Challenges Encountered & Solutions

### 1. **NLTK Data Management in Docker**
**Challenge**: NLTK requires data downloads that can fail in containerized environments
**Solution**: Pre-download NLTK data during Docker build process and set custom data paths with proper user permissions

### 2. **LLM API Integration & Reliability**
**Challenge**: Dependence on external APIs can cause failures and inconsistent responses
**Solution**: Implemented robust fallback system using template-based generation when LLM APIs are unavailable, with intelligent response cleaning

### 3. **Multi-User Session Management**
**Challenge**: Web interface needs to maintain separate agent instances per user
**Solution**: UUID-based session management with isolated agent storage per session

### 4. **Realistic F1 Behaviour Simulation**
**Challenge**: Generating authentic F1 driver responses across different scenarios and contexts
**Solution**: Comprehensive F1 data integration with context-aware message generation, mood-based response adaptation, and circuit-specific challenge mapping

### 5. **Production Deployment & Security**
**Challenge**: Balancing functionality with security and performance in containerized deployment
**Solution**: Multi-stage Docker build, non-root user execution, health checks, optimized dependency management, and comprehensive error handling

### 6. **Context Continuity**
**Challenge**: Maintaining realistic context progression throughout race weekends
**Solution**: Dynamic context updates with automatic mood adjustment based on performance, incident tracking, and session-to-session continuity

## Technical Stack

- **Core Language**: Python 3.11
- **Web Framework**: Flask with session management
- **NLP**: NLTK with VADER sentiment analysis
- **LLM Integration**: Mistral API with requests library
- **UI Enhancement**: Rich library for CLI experience
- **Containerization**: Docker with multi-stage builds and security hardening
- **Data Management**: Python dataclasses, enums, and JSON serialization

## Project Structure
```
f1_racer_ai_agent/
├── f1_agent.py          # Core agent implementation with CLI
├── f1_data.py           # F1 data structures and utilities
├── app.py               # Flask web application
├── run_web.py           # Web interface launcher
├── test_agent.py        # Comprehensive test suite
├── templates/           # HTML templates for web interface
├── static/              # CSS and JavaScript assets
├── requirements.txt     # Python dependencies
├── Dockerfile           # Multi-stage container configuration
├── docker-compose.yml   # Container orchestration
├── .env.example         # Environment variables template
└── README.md           # This documentation
```