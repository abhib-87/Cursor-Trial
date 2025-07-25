# Trip Planner Agent using LangGraph

A comprehensive trip planning system built with LangGraph that uses multiple specialized AI agents to create detailed travel itineraries. Instead of CrewAI, this implementation leverages LangGraph's powerful workflow orchestration to coordinate different planning aspects.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for research, accommodations, activities, itinerary planning, budgeting, and travel tips
- **LangGraph Workflow**: Sophisticated state management and agent coordination
- **Comprehensive Planning**: Complete trip plans including accommodations, daily itineraries, budget breakdowns, and travel tips
- **Flexible Input**: Support for different trip types, budgets, and preferences
- **Rich Output**: Formatted trip plans with detailed information and export capabilities

## 🏗️ Architecture

The trip planner uses six specialized agents orchestrated by LangGraph:

1. **Research Agent**: Gathers destination information, weather, culture, and general travel data
2. **Accommodation Agent**: Finds suitable lodging options based on budget and preferences
3. **Activity Agent**: Discovers attractions, activities, and experiences
4. **Itinerary Agent**: Creates day-by-day schedules optimizing time and logistics
5. **Budget Agent**: Calculates cost estimates and provides budget breakdowns
6. **Travel Tips Agent**: Generates packing lists, safety tips, and local advice

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Required packages (see `requirements.txt`)

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trip-planner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 💡 Usage

### Basic Example

```python
from datetime import date, timedelta
from trip_planner import TripRequest, TripType, BudgetRange, create_trip_planner
from trip_planner.utils import format_trip_plan

# Create a trip request
trip_request = TripRequest(
    destination="Tokyo, Japan",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=37),
    budget=BudgetRange.MODERATE,
    trip_type=TripType.CULTURAL,
    travelers=2,
    preferences=["temples", "food", "technology"],
    dietary_restrictions=["vegetarian"]
)

# Create and run the trip planner
planner = create_trip_planner()
result = planner.plan_trip(trip_request)

# Display the plan
if result.final_plan:
    print(format_trip_plan(result.final_plan))
```

### Running the Example

```bash
# Run with sample data
python example.py

# Interactive mode
python example.py
# Choose option 2 for interactive input
```

## 📊 Trip Request Parameters

- **destination**: Target city or country
- **start_date** / **end_date**: Travel dates
- **budget**: `BUDGET`, `MODERATE`, or `LUXURY`
- **trip_type**: `LEISURE`, `BUSINESS`, `ADVENTURE`, `CULTURAL`, `ROMANTIC`, or `FAMILY`
- **travelers**: Number of people
- **preferences**: List of interests (e.g., ["art", "food", "hiking"])
- **dietary_restrictions**: List of dietary needs (optional)
- **mobility_requirements**: Special accessibility needs (optional)

## 🎯 Output Structure

The trip planner generates comprehensive plans including:

### Accommodations
- Hotel/lodging recommendations
- Price ranges and ratings
- Amenities and booking information

### Daily Itinerary
- Day-by-day activity schedules
- Meal recommendations
- Transportation suggestions
- Timing and logistics

### Budget Breakdown
- Cost estimates by category
- Total trip cost projections
- Money-saving tips

### Travel Information
- Packing suggestions
- Safety advice
- Emergency contacts
- Cultural etiquette tips

## 🔧 Customization

### Adding New Agents

```python
from trip_planner.agents import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        # Custom initialization
    
    def custom_method(self, state: AgentState):
        # Custom agent logic
        pass
```

### Modifying the Workflow

```python
from trip_planner.graph import TripPlannerGraph

class CustomTripPlanner(TripPlannerGraph):
    def _build_graph(self):
        # Custom workflow definition
        workflow = super()._build_graph()
        # Add custom nodes and edges
        return workflow
```

## 📁 Project Structure

```
trip-planner/
├── trip_planner/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Pydantic data models
│   ├── agents.py            # Specialized AI agents
│   ├── graph.py             # LangGraph workflow
│   └── utils.py             # Utility functions
├── example.py               # Usage examples
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md               # Documentation
```

## 🔐 Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for enhanced functionality)
SERPAPI_KEY=your_serpapi_key_here
WEATHER_API_KEY=your_weather_api_key_here
```

## 🚨 Error Handling

The system includes comprehensive error handling:

- Individual agent failures don't stop the entire workflow
- Errors are collected and reported in the final state
- Graceful degradation when some information isn't available
- Detailed error messages for debugging

## 🎨 Example Output

```
============================================================
🌍 TRIP PLAN: PARIS, FRANCE
============================================================
📅 Duration: 2024-02-15 to 2024-02-21 (7 days)

🏨 ACCOMMODATIONS
------------------------------
1. Hotel des Grands Boulevards (hotel)
   📍 Central Paris, 2nd Arrondissement
   💰 €150-200/night
   ⭐ 4.5/5
   🎯 Amenities: wifi, breakfast, concierge

📅 DAILY ITINERARY
------------------------------
Day 1 - Thursday, February 15, 2024
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
🎯 Louvre Museum
   📍 1st Arrondissement
   ⏱️ 3-4 hours
   💰 €17
   📝 World's largest art museum...

💰 BUDGET BREAKDOWN
------------------------------
🏨 Accommodation: €1,050-1,400
🚗 Transportation: €200-300
🎯 Activities: €300-500
🍽️ Meals: €700-1,000
🛍️ Miscellaneous: €200-300
--------------------
💵 TOTAL ESTIMATE: €2,450-3,500

💡 TRAVEL TIPS
------------------------------
• Book museum tickets in advance
• Learn basic French phrases
• Carry a reusable water bottle
...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error messages and system information

## 🔮 Future Enhancements

- [ ] Integration with real booking APIs
- [ ] Weather-based activity recommendations
- [ ] Multi-language support
- [ ] Mobile app interface
- [ ] Collaborative trip planning
- [ ] Integration with calendar apps
- [ ] Real-time price monitoring
- [ ] Social features and reviews
