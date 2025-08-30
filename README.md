# Traveler Planner Agent

A smart AI-powered travel planning agent that uses LangGraph workflows to help users plan their trips with intelligent research and recommendations.

## Overview

This project implements an AI agent system that can help users plan travels by leveraging internet search capabilities and intelligent conversation flows. The system uses a modular architecture with specialized agents and nodes for different functionalities.

## Project Structure

```
traveler_planner_agent/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables (not in repo)
├── .env.template                      # Environment variables template
├── template.py                        # Project structure generator
├── state/
│   └── state.py                       # Application state management
├── tools/
│   ├── general_agent.py               # General purpose agent tools
│   └── internet_search_agent.py       # Internet search capabilities
├── node/
│   ├── general_agent_node.py          # General agent workflow nodes
│   └── internet_search_node.py        # Internet search workflow nodes
├── prompt/
│   ├── general_agent_prompt.py        # Prompts for general agent
│   └── internet_search_prompt.py      # Prompts for search agent
├── memories/
│   └── memories.py                    # Conversation and context memory
├── workflow/
│   └── langgraph_workflow.py          # Main LangGraph workflow definition
└── utils/
    ├── llm.py                         # LLM configuration and utilities
    └── conversion_summarizer.py       # Text conversion and summarization
```

## Features

- **Intelligent Travel Planning**: AI-powered agent that understands travel requirements
- **Internet Search Integration**: Real-time web search for up-to-date travel information
- **Memory System**: Maintains context and conversation history
- **Modular Architecture**: Extensible design with specialized agents and tools
- **LangGraph Workflows**: Advanced workflow management for complex agent interactions

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd traveler_planner_agent
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```bash
    cp .env.template .env
    # Edit .env file with your API keys and configurations
    ```

## Configuration

Copy `.env.template` to `.env` and configure the following variables:

```env
# Add your API keys and configuration here
OPENAI_API_KEY=your_openai_api_key
SEARCH_API_KEY=your_search_api_key
# Add other required environment variables
```

## Usage

### Quick Start

```python
from workflow.langgraph_workflow import TravelerPlannerWorkflow

# Initialize the workflow
planner = TravelerPlannerWorkflow()

# Start planning a trip
result = planner.plan_trip("I want to visit Japan for 10 days in spring")
print(result)


# Example Response

Here is a detailed 10-day Japan trip plan from India for you and your wife, covering transportation, accommodation, daily itinerary, budget, practical info, local transport, and dining recommendations for 2025.

---

### 1. Transportation

- **Round-trip Flights (India to Japan):**  
    From major Indian cities (Delhi, Mumbai, Bangalore), round-trip economy flights to Tokyo (Narita or Haneda) typically cost around **₹40,000 to ₹60,000 per person** in 2025, depending on booking time and airline (e.g., ANA, Japan Airlines, Air India). Booking 2-3 months in advance is recommended for best fares.

- **Airport Transfers:**  
    From Narita Airport to Tokyo city center:  
    - Narita Express train: ~¥3,000 (~₹1,800) per person, 60-90 minutes  
    - Limousine bus: ~¥3,200 (~₹1,900) per person  
    From Kansai Airport (if flying out from Osaka):  
    - JR Haruka Express: ~¥3,000 (~₹1,800) per person

---

### 2. Accommodation (10 nights)

| Category       | Location           | Hotel Suggestions                      | Price Range (per night)          |
|----------------|--------------------|--------------------------------------|---------------------------------|
| Budget         | Tokyo, Kyoto, Osaka| Business hotels like APA, Toyoko Inn | ₹3,000 - ₹5,000                 |
| Mid-range      | Tokyo, Kyoto, Osaka| Hotel Gracery Shinjuku, Hotel Mystays| ₹7,000 - ₹12,000                |
| Luxury         | Tokyo, Kyoto, Osaka| Park Hyatt Tokyo, The Ritz-Carlton Kyoto| ₹20,000 - ₹40,000+             |

*Recommended to split nights roughly as: Tokyo (4), Kyoto (3), Osaka (3)*

---

### 3. Daily Itinerary

**Day 1: Arrival Tokyo**
- Arrive Narita/Haneda, transfer to hotel
- Relax or short visit to Shinjuku or Ginza for dinner

**Day 2: Tokyo Highlights**
- Asakusa Temple & Nakamise Street
- Tokyo Skytree Observation Deck
- Ueno Park and Museums
- Evening at Shibuya Crossing and Hachiko Statue

**Day 3: Tokyo Day Trips**
- Day trip to Nikko (UNESCO World Heritage) or Kamakura (Great Buddha)

**Day 4: Mt. Fuji & Hakone**
- Travel to Hakone (using Hakone Free Pass)
- Lake Ashi Cruise, Hakone Ropeway, Onsen experience
- Overnight in Hakone or return to Tokyo

**Day 5: Tokyo to Kyoto**
- Shinkansen (bullet train) to Kyoto (~2.5 hours)
- Visit Fushimi Inari Shrine
- Evening stroll in Gion district

**Day 6: Kyoto Cultural Tour**
- Kinkaku-ji (Golden Pavilion)
- Arashiyama Bamboo Forest
- Nijo Castle

**Day 7: Nara Day Trip**
- Visit Todai-ji Temple, Nara Park (deer park)
- Return to Kyoto

**Day 8: Kyoto to Osaka**
- Travel to Osaka (~15 minutes by train)
- Explore Dotonbori area, try street food
- Visit Osaka Castle

**Day 9: Osaka Exploration**
- Kaiyukan Aquarium
- Tempozan Ferris Wheel
- Shopping in Shinsaibashi

**Day 10: Departure**
- Transfer to Kansai Airport for flight back to India

---

### 4. Budget Breakdown (Per Couple Approximate)

| Expense               | Cost (₹)          |
|-----------------------|-------------------|
| Flights (round trip)   | 1,00,000          |
| Accommodation (10 nights, mid-range) | 80,000           |
| Local Transport (JR Pass 7 days + local) | 20,000           |
| Meals (₹1,500 per day per person) | 30,000           |
| Activities & Entry Fees | 15,000           |
| Miscellaneous & Shopping | 15,000           |
| **Total Estimated Cost** | **2,60,000 - 2,70,000** |

---

### 5. Practical Information

- **Visa:** Indian citizens require a tourist visa for Japan. Apply online or at the Japanese embassy; processing takes about 5-7 working days. Visa fee approx. ₹1,000-₹2,000.
- **Currency:** Japanese Yen (JPY). 1 INR ≈ 1.5 JPY (varies). ATMs widely available; credit cards accepted in many places.
- **Local Customs:** Bowing is common; remove shoes indoors; quiet demeanor in public transport.
- **Safety:** Japan is very safe; standard travel precautions apply.
- **Weather:** September is late summer/early autumn; expect mild to warm weather (20-28°C), occasional rain. Pack light layers and rain gear.

---

### 6. Local Transport

- **Japan Rail Pass:** Highly recommended 7-day JR Pass (~¥29,650 ≈ ₹15,000) for Shinkansen and JR trains covering Tokyo-Kyoto-Osaka and day trips. Activate on Day 4 or 5 to cover long-distance travel.
- **Local Metro/Bus:** Tokyo Metro day passes (~¥600), Kyoto buses (~¥230 per ride), Osaka Metro day passes (~¥800).
- **Taxis:** Expensive (~¥410 for first 1 km), use only for convenience or late night.

---

### 7. Food & Dining

- **Local Specialties:** Sushi, ramen, tempura, okonomiyaki (Osaka), kaiseki (Kyoto), matcha sweets.
- **Recommended Restaurants:**
    - Tokyo: Sushi Zanmai (affordable sushi), Ichiran Ramen
    - Kyoto: Nishiki Market for street food, Gion Kappa Restaurant
    - Osaka: Dotonbori street food stalls, Kani Doraku (crab specialty)
- **Meal Costs:**
    - Budget meals: ¥800-¥1,200 (~₹500-₹750) per person
    - Mid-range restaurants: ¥2,000-¥4,000 (~₹1,200-₹2,400) per person

---

This plan balances cultural immersion, iconic sights, and comfortable travel for a memorable 10-day trip to Japan from India with your wife in 2025. Adjust accommodation and activities based on your preferences and budget.
```

### Project Setup

If you're setting up the project structure from scratch, run:

```bash
python template.py
```

This will create all the necessary directories and files.

## Architecture

### Components

- **State Management**: Centralized state handling for agent interactions
- **Agent Tools**: Specialized tools for different functionalities
- **Workflow Nodes**: Individual processing units in the LangGraph workflow
- **Prompts**: Carefully crafted prompts for different agent types
- **Memory System**: Context preservation across conversations
- **Utilities**: Helper functions for LLM operations and text processing

### Workflow

1. User provides travel requirements
2. General agent processes the request
3. Internet search agent gathers relevant information
4. Information is processed and summarized
5. Comprehensive travel plan is generated
6. Results are stored in memory for future reference

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License

## Support

For questions and support, please aakashsyadav1999@gmail.com
