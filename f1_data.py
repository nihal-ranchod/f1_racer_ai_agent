#!/usr/bin/env python3
"""
F1 Data Module - Realistic Formula 1 data for enhanced agent accuracy

This module contains authentic F1 data including:
- Current teams and drivers (2025 season)
- Circuit information and characteristics  
- Race weekend session structure
- Technical terminology and regulations
- Historical context and rivalries

Author: Enhanced F1 AI Agent
Date: 2025
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import random

class SessionType(Enum):
    """Realistic F1 session types"""
    FP1 = "fp1"
    FP2 = "fp2"
    FP3 = "fp3"
    SPRINT_SHOOTOUT = "sprint_shootout"  # New format
    SPRINT_RACE = "sprint_race"
    QUALIFYING = "qualifying"
    RACE = "race"

class WeatherCondition(Enum):
    """Weather conditions affecting F1 races"""
    DRY = "dry"
    WET = "wet"
    MIXED = "mixed"
    OVERCAST = "overcast"

class TyreCompound(Enum):
    """Pirelli tyre compounds"""
    C1 = "hard"
    C2 = "medium"  
    C3 = "soft"
    INTERMEDIATE = "intermediate"
    WET = "wet"

@dataclass
class Circuit:
    """F1 Circuit information"""
    name: str
    country: str
    city: str
    length_km: float
    corners: int
    drs_zones: int
    characteristics: List[str]
    lap_record: str
    difficulty: str  # "high", "medium", "low"

@dataclass
class Team:
    """F1 Team information"""
    name: str
    short_name: str
    engine: str
    principal: str
    drivers: List[str]
    colors: List[str]
    championship_wins: int

@dataclass
class SessionResult:
    """Result from a practice/qualifying session"""
    position: int
    gap_to_leader: Optional[str]
    best_time: str
    laps_completed: int
    incidents: List[str]

# 2025 F1 Teams and Drivers
F1_TEAMS = {
    "red_bull": Team(
        name="Red Bull Racing",
        short_name="RBR",
        engine="Honda RBPT",
        principal="Christian Horner",
        drivers=["Max Verstappen", "Liam Lawson"],  # Tsunoda mid-season swap possible
        colors=["navy", "red", "yellow"],
        championship_wins=6
    ),
    "ferrari": Team(
        name="Scuderia Ferrari",
        short_name="Ferrari",
        engine="Ferrari",
        principal="Frédéric Vasseur",
        drivers=["Charles Leclerc", "Lewis Hamilton"],
        colors=["red"],
        championship_wins=16
    ),
    "mercedes": Team(
        name="Mercedes-AMG Petronas F1 Team",
        short_name="Mercedes",
        engine="Mercedes",
        principal="Toto Wolff",
        drivers=["George Russell", "Kimi Antonelli"],
        colors=["silver", "black", "turquoise"],
        championship_wins=8
    ),
    "mclaren": Team(
        name="McLaren F1 Team",
        short_name="McLaren",
        engine="Mercedes",
        principal="Andrea Stella",
        drivers=["Lando Norris", "Oscar Piastri"],
        colors=["orange", "blue"],
        championship_wins=8
    ),
    "aston_martin": Team(
        name="Aston Martin Aramco Cognizant F1 Team",
        short_name="Aston Martin",
        engine="Mercedes",
        principal="Mike Krack",
        drivers=["Fernando Alonso", "Lance Stroll"],
        colors=["green"],
        championship_wins=0
    ),
    "alpine": Team(
        name="BWT Alpine F1 Team",
        short_name="Alpine",
        engine="Renault",
        principal="Bruno Famin",
        drivers=["Pierre Gasly", "Franco Colapinto"],  # rotating seat
        colors=["blue", "pink"],
        championship_wins=2
    ),
    "williams": Team(
        name="Williams Racing",
        short_name="Williams",
        engine="Mercedes",
        principal="James Vowles",
        drivers=["Alex Albon", "Carlos Sainz"],
        colors=["blue", "white"],
        championship_wins=9
    ),
    "racing_bulls": Team(
        name="Racing Bulls",
        short_name="RB",
        engine="Honda RBPT",
        principal="Laurent Mekies",
        drivers=["Yuki Tsunoda", "Isack Hadjar"],
        colors=["white", "blue"],
        championship_wins=0
    ),
    "haas": Team(
        name="MoneyGram Haas F1 Team",
        short_name="Haas",
        engine="Ferrari",
        principal="Ayao Komatsu",
        drivers=["Esteban Ocon", "Oliver Bearman"],
        colors=["white", "red", "blue"],
        championship_wins=0
    )
}

# 2025 F1 Calendar (24 races)
F1_CIRCUITS = {
    "australia": Circuit(
        name="Albert Park Circuit",
        country="Australia",
        city="Melbourne",
        length_km=5.278,
        corners=14,
        drs_zones=4,
        characteristics=["semi-street", "fast", "bumpy", "unpredictable-weather"],
        lap_record="1:20.260 (Charles Leclerc, 2022)",
        difficulty="medium"
    ),
    "china": Circuit(
        name="Shanghai International Circuit",
        country="China",
        city="Shanghai",
        length_km=5.451,
        corners=16,
        drs_zones=2,
        characteristics=["long-straights", "technical", "overtaking-opportunities"],
        lap_record="1:32.238 (Michael Schumacher, 2004)",
        difficulty="medium"
    ),
    "japan": Circuit(
        name="Suzuka International Racing Course",
        country="Japan",
        city="Suzuka",
        length_km=5.807,
        corners=18,
        drs_zones=2,
        characteristics=["figure-eight", "technical", "challenging", "130r-corner"],
        lap_record="1:30.983 (Lewis Hamilton, 2019)",
        difficulty="high"
    ),
    "bahrain": Circuit(
        name="Bahrain International Circuit",
        country="Bahrain",
        city="Sakhir",
        length_km=5.412,
        corners=15,
        drs_zones=3,
        characteristics=["high-speed", "desert", "night-race", "overtaking-opportunities"],
        lap_record="1:31.447 (Pedro de la Rosa, 2005)",
        difficulty="medium"
    ),
    "saudi_arabia": Circuit(
        name="Jeddah Corniche Circuit",
        country="Saudi Arabia",
        city="Jeddah",
        length_km=6.174,
        corners=27,
        drs_zones=3,
        characteristics=["street-circuit", "high-speed", "narrow", "dangerous"],
        lap_record="1:30.734 (Lewis Hamilton, 2021)",
        difficulty="high"
    ),
    "miami": Circuit(
        name="Miami International Autodrome",
        country="United States",
        city="Miami",
        length_km=5.412,
        corners=19,
        drs_zones=3,
        characteristics=["street-circuit", "hot", "showbiz", "long-straights"],
        lap_record="1:29.708 (Max Verstappen, 2023)",
        difficulty="medium"
    ),
    "imola": Circuit(
        name="Autodromo Enzo e Dino Ferrari",
        country="Italy",
        city="Imola",
        length_km=4.909,
        corners=19,
        drs_zones=1,
        characteristics=["historic", "technical", "fast chicanes"],
        lap_record="1:15.484 (Lewis Hamilton, 2020)",
        difficulty="high"
    ),
    "monaco": Circuit(
        name="Circuit de Monaco",
        country="Monaco",
        city="Monte Carlo",
        length_km=3.337,
        corners=19,
        drs_zones=1,
        characteristics=["street-circuit", "narrow", "prestigious", "difficult-overtaking"],
        lap_record="1:12.909 (Lewis Hamilton, 2019)",
        difficulty="high"
    ),
    "spain": Circuit(
        name="Circuit de Barcelona-Catalunya",
        country="Spain",
        city="Barcelona",
        length_km=4.675,
        corners=14,
        drs_zones=2,
        characteristics=["testing-circuit", "balanced", "aero-demanding"],
        lap_record="1:18.149 (Max Verstappen, 2023)",
        difficulty="medium"
    ),
    "canada": Circuit(
        name="Circuit Gilles Villeneuve",
        country="Canada",
        city="Montreal",
        length_km=4.361,
        corners=14,
        drs_zones=3,
        characteristics=["stop-go", "walls", "late-braking", "Wall of Champions"],
        lap_record="1:13.078 (Valtteri Bottas, 2019)",
        difficulty="medium"
    ),
    "austria": Circuit(
        name="Red Bull Ring",
        country="Austria",
        city="Spielberg",
        length_km=4.318,
        corners=10,
        drs_zones=3,
        characteristics=["short-lap", "elevation", "power-track"],
        lap_record="1:05.619 (Carlos Sainz, 2020)",
        difficulty="medium"
    ),
    "silverstone": Circuit(
        name="Silverstone Circuit",
        country="United Kingdom",
        city="Silverstone",
        length_km=5.891,
        corners=18,
        drs_zones=2,
        characteristics=["high-speed", "historic", "home-of-f1", "challenging-corners"],
        lap_record="1:27.097 (Max Verstappen, 2020)",
        difficulty="high"
    ),
    "spa": Circuit(
        name="Circuit de Spa-Francorchamps",
        country="Belgium",
        city="Stavelot",
        length_km=7.004,
        corners=20,
        drs_zones=2,
        characteristics=["longest-circuit", "historic", "eau-rouge", "weather-unpredictable"],
        lap_record="1:46.286 (Valtteri Bottas, 2018)",
        difficulty="high"
    ),
    "hungary": Circuit(
        name="Hungaroring",
        country="Hungary",
        city="Budapest",
        length_km=4.381,
        corners=14,
        drs_zones=1,
        characteristics=["twisty", "slow", "technical"],
        lap_record="1:16.627 (Lewis Hamilton, 2020)",
        difficulty="medium"
    ),
    "netherlands": Circuit(
        name="Circuit Zandvoort",
        country="Netherlands",
        city="Zandvoort",
        length_km=4.259,
        corners=14,
        drs_zones=2,
        characteristics=["banked-corners", "narrow", "technical"],
        lap_record="1:11.097 (Lewis Hamilton, 2021)",
        difficulty="medium"
    ),
    "monza": Circuit(
        name="Autodromo Nazionale di Monza",
        country="Italy",
        city="Monza",
        length_km=5.793,
        corners=11,
        drs_zones=3,
        characteristics=["temple-of-speed", "low-downforce", "historic", "passionate-fans"],
        lap_record="1:21.046 (Rubens Barrichello, 2004)",
        difficulty="medium"
    ),
    "baku": Circuit(
        name="Baku City Circuit",
        country="Azerbaijan",
        city="Baku",
        length_km=6.003,
        corners=20,
        drs_zones=2,
        characteristics=["street-circuit", "long-straight", "castle-section"],
        lap_record="1:43.009 (Charles Leclerc, 2019)",
        difficulty="high"
    ),
    "singapore": Circuit(
        name="Marina Bay Street Circuit",
        country="Singapore",
        city="Singapore",
        length_km=4.940,
        corners=19,
        drs_zones=2,
        characteristics=["night-race", "street-circuit", "humid"],
        lap_record="1:41.905 (Kevin Magnussen, 2018)",
        difficulty="high"
    ),
    "austin": Circuit(
        name="Circuit of the Americas",
        country="United States",
        city="Austin",
        length_km=5.513,
        corners=20,
        drs_zones=2,
        characteristics=["modern", "elevation", "fast-sweepers"],
        lap_record="1:36.169 (Charles Leclerc, 2019)",
        difficulty="medium"
    ),
    "mexico": Circuit(
        name="Autódromo Hermanos Rodríguez",
        country="Mexico",
        city="Mexico City",
        length_km=4.304,
        corners=17,
        drs_zones=2,
        characteristics=["high-altitude", "long-straight", "stadium-section"],
        lap_record="1:17.774 (Valtteri Bottas, 2021)",
        difficulty="medium"
    ),
    "brazil": Circuit(
        name="Autódromo José Carlos Pace",
        country="Brazil",
        city="São Paulo",
        length_km=4.309,
        corners=15,
        drs_zones=2,
        characteristics=["anti-clockwise", "elevation-changes", "passionate-fans", "unpredictable-weather"],
        lap_record="1:10.540 (Valtteri Bottas, 2018)",
        difficulty="medium"
    ),
    "las_vegas": Circuit(
        name="Las Vegas Strip Circuit",
        country="United States",
        city="Las Vegas",
        length_km=6.201,
        corners=17,
        drs_zones=3,
        characteristics=["street-circuit", "night-race", "long-straights", "showbiz"],
        lap_record="1:35.490 (Oscar Piastri, 2023)",
        difficulty="medium"
    ),
    "qatar": Circuit(
        name="Lusail International Circuit",
        country="Qatar",
        city="Lusail",
        length_km=5.419,
        corners=16,
        drs_zones=2,
        characteristics=["night-race", "fast", "desert"],
        lap_record="1:23.196 (Max Verstappen, 2021)",
        difficulty="medium"
    ),
    "abu_dhabi": Circuit(
        name="Yas Marina Circuit",
        country="United Arab Emirates",
        city="Abu Dhabi",
        length_km=5.281,
        corners=16,
        drs_zones=2,
        characteristics=["twilight-race", "modern-facilities", "title-decider", "marina"],
        lap_record="1:26.103 (Max Verstappen, 2021)",
        difficulty="medium"
    )
}

# Enhanced F1 Terminology and Context
F1_TECHNICAL_TERMS = {
    "aerodynamics": ["downforce", "drag", "ground effect", "porpoising", "dirty air", "slipstream"],
    "tyres": ["degradation", "graining", "blistering", "thermal window", "compound selection", "stint"],
    "strategy": ["undercut", "overcut", "pit window", "track position", "tyre delta", "safety car"],
    "performance": ["sector times", "mini-sectors", "purple sectors", "personal best", "track evolution"],
    "incidents": ["lock-up", "flat-spot", "spin", "off-track", "contact", "damage assessment"],
    "conditions": ["track temperature", "ambient temperature", "wind direction", "grip levels", "track surface"]
}

F1_RADIO_PHRASES = [
    "Box, box, box!",
    "Stay out, stay out!",
    "Push now, push!",
    "We are checking",
    "Gap to car behind",
    "DRS is available",
    "Yellow flags in sector 2",
    "Safety car, safety car",
    "Virtual safety car",
    "Keep your head down",
    "Hammer time!",
    "That's pole position!",
    "P1! P1! Yes!",
    "Simply lovely"
]

F1_EMOTIONS_CONTEXT = {
    "victory": ["ecstatic", "overwhelming", "dream come true", "speechless", "incredible team effort"],
    "podium": ["thrilled", "proud", "solid performance", "great team work", "building momentum"],
    "points": ["satisfied", "progress", "step forward", "good execution", "positive direction"],
    "no_points": ["disappointed", "frustrated", "we'll bounce back", "analyze and improve", "tough day"],
    "dnf": ["heartbroken", "mechanical issues", "racing incident", "that's motor racing", "regroup"]
}

# Real F1 Weekend Structure (Current Format)
RACE_WEEKEND_SESSIONS = {
    "standard_weekend": [
        {"session": SessionType.FP1, "duration": 90, "day": "Friday"},
        {"session": SessionType.FP2, "duration": 90, "day": "Friday"}, 
        {"session": SessionType.FP3, "duration": 60, "day": "Saturday"},
        {"session": SessionType.QUALIFYING, "duration": 60, "day": "Saturday"},
        {"session": SessionType.RACE, "duration": 120, "day": "Sunday"}
    ],
    "sprint_weekend": [
        {"session": SessionType.FP1, "duration": 90, "day": "Friday"},
        {"session": SessionType.SPRINT_SHOOTOUT, "duration": 45, "day": "Friday"},
        {"session": SessionType.SPRINT_RACE, "duration": 100, "day": "Saturday"},
        {"session": SessionType.QUALIFYING, "duration": 60, "day": "Saturday"},
        {"session": SessionType.RACE, "duration": 120, "day": "Sunday"}
    ]
}

def get_realistic_session_result(session_type: SessionType, team_performance: str = "midfield") -> SessionResult:
    """Generate realistic session results based on team performance"""
    
    # Position ranges based on team performance
    position_ranges = {
        "top_team": (1, 6),
        "midfield": (7, 15), 
        "backmarker": (16, 20)
    }
    
    pos_range = position_ranges.get(team_performance, (7, 15))
    position = random.randint(*pos_range)
    
    # Realistic lap times and gaps
    if session_type == SessionType.QUALIFYING:
        gaps = ["+0.000", "+0.123", "+0.287", "+0.445", "+0.567", "+0.789", "+1.234", "+1.567", "+2.123"]
        gap = gaps[min(position-1, len(gaps)-1)] if position > 1 else None
        best_time = "1:23.456"
        laps = random.randint(8, 12)
    else:  # Practice sessions
        gap = f"+{random.uniform(0.1, 3.0):.3f}" if position > 1 else None
        best_time = f"1:{random.randint(22, 26)}.{random.randint(100, 999)}"
        laps = random.randint(15, 35)
    
    # Realistic incidents
    incident_pool = ["lock-up turn 1", "flat-spot front left", "off-track limits turn 4", 
                    "yellow flag sector 2", "traffic in final sector"]
    incidents = random.sample(incident_pool, k=random.randint(0, 2))
    
    return SessionResult(
        position=position,
        gap_to_leader=gap,
        best_time=best_time, 
        laps_completed=laps,
        incidents=incidents
    )

def get_circuit_specific_challenges(circuit_name: str) -> List[str]:
    """Get specific challenges for each circuit"""
    circuit = F1_CIRCUITS.get(circuit_name)
    if not circuit:
        return ["setup challenges", "tyre management"]
    
    challenges = []
    if "narrow" in circuit.characteristics:
        challenges.extend(["track positioning crucial", "limited overtaking"])
    if "high-speed" in circuit.characteristics:
        challenges.extend(["aerodynamic efficiency key", "slipstream battles"])
    if "street-circuit" in circuit.characteristics:
        challenges.extend(["barrier proximity", "no run-off areas"])
    if "weather-unpredictable" in circuit.characteristics:
        challenges.extend(["weather decisions critical", "tyre strategy complex"])
    
    return challenges[:3]  # Return top 3 challenges

def get_teammate_name(driver_name: str) -> Optional[str]:
    """Get teammate name for a given driver"""
    for team in F1_TEAMS.values():
        if driver_name in team.drivers:
            teammates = [d for d in team.drivers if d != driver_name]
            return teammates[0] if teammates else None
    return None

def get_team_by_driver(driver_name: str) -> Optional[Team]:
    """Get team information by driver name"""
    for team in F1_TEAMS.values():
        if driver_name in team.drivers:
            return team
    return None

def get_random_competitor(exclude_driver: str) -> str:
    """Get random competitor driver name excluding specified driver"""
    all_drivers = []
    for team in F1_TEAMS.values():
        all_drivers.extend(team.drivers)
    
    competitors = [d for d in all_drivers if d != exclude_driver]
    return random.choice(competitors) if competitors else "Lewis Hamilton"