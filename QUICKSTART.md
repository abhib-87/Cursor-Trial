# Quick Start Guide

## 🚀 Getting Started with the Trip Planner

### 1. Installation

```bash
# Create and activate virtual environment
python3 -m venv trip_planner_env
source trip_planner_env/bin/activate  # On Windows: trip_planner_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set up API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Example

```bash
# Run with sample data
python example.py

# Choose option 1 for sample data or option 2 for interactive input
```

### 4. Basic Usage

```python
from datetime import date, timedelta
from trip_planner import TripRequest, TripType, BudgetRange, create_trip_planner
from trip_planner.utils import format_trip_plan

# Create a trip request
trip_request = TripRequest(
    destination="Paris, France",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=37),
    budget=BudgetRange.MODERATE,
    trip_type=TripType.CULTURAL,
    travelers=2,
    preferences=["art", "museums", "cuisine"],
    dietary_restrictions=["vegetarian"]
)

# Create and run the trip planner
planner = create_trip_planner()
result = planner.plan_trip(trip_request)

# Display the plan
if result.final_plan:
    print(format_trip_plan(result.final_plan))
```

### 5. Customization

You can customize various aspects:

- **Trip Types**: `LEISURE`, `BUSINESS`, `ADVENTURE`, `CULTURAL`, `ROMANTIC`, `FAMILY`
- **Budget Levels**: `BUDGET`, `MODERATE`, `LUXURY`
- **Preferences**: List of interests like `["food", "history", "nightlife", "nature"]`
- **Dietary Restrictions**: List like `["vegetarian", "gluten-free", "halal"]`

### 6. Output Features

The trip planner generates:

- 🏨 **Accommodation recommendations** with ratings and amenities
- 📅 **Day-by-day itineraries** with optimized scheduling
- 🎯 **Activity suggestions** based on preferences and trip type
- 💰 **Budget breakdowns** with cost estimates
- 💡 **Travel tips** and packing suggestions
- 🚨 **Emergency contacts** and safety information

### 7. Saving Plans

```python
from trip_planner.utils import save_trip_plan

# Save to JSON file
filename = save_trip_plan(result.final_plan)
print(f"Plan saved to: {filename}")
```

### 8. Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is set in the `.env` file
- **Import Errors**: Ensure you're in the virtual environment and dependencies are installed
- **Planning Errors**: Check your internet connection and API key validity

---

🎉 **You're all set!** Start planning amazing trips with your LangGraph-powered trip planner!