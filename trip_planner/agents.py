from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseMessage
from langchain.schema.output_parser import StrOutputParser
import json
import re
from datetime import datetime, timedelta

from .models import (
    AgentState, TripRequest, Activity, Accommodation, 
    Transportation, BudgetBreakdown, DayItinerary, TripPlan
)


class BaseAgent:
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)
        self.output_parser = StrOutputParser()

    def _parse_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extract JSON from LLM response, handling various formats."""
        try:
            # Try to parse the entire response as JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # Look for JSON within the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            # If no valid JSON found, return a structured error
            return {"error": "Could not parse JSON from response", "raw_response": response}


class ResearchAgent(BaseAgent):
    """Agent responsible for researching destinations and gathering travel information."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a travel research expert. Your job is to research destinations and provide comprehensive information for trip planning.

You should provide information about:
- Best time to visit
- Climate and weather
- Popular attractions and activities
- Local culture and customs
- Transportation options
- Safety considerations
- Currency and typical costs
- Language and communication
- Local cuisine highlights

Return your response as a JSON object with the following structure:
{
    "destination": "destination name",
    "best_time_to_visit": "description",
    "climate": "description",
    "attractions": ["list of attractions"],
    "culture_tips": ["list of cultural tips"],
    "transportation": "transportation overview",
    "safety": "safety information",
    "currency": "currency info",
    "language": "language info",
    "cuisine": ["local dishes/restaurants"],
    "estimated_daily_cost": {
        "budget": "amount",
        "moderate": "amount", 
        "luxury": "amount"
    }
}"""),
            ("human", "Research information for a trip to {destination}. The trip is for {travelers} travelers, budget level: {budget}, trip type: {trip_type}. Trip dates: {start_date} to {end_date}.")
        ])

    def research_destination(self, state: AgentState) -> Dict[str, Any]:
        """Research the destination and return comprehensive information."""
        request = state.trip_request
        
        chain = self.prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "destination": request.destination,
            "travelers": request.travelers,
            "budget": request.budget.value,
            "trip_type": request.trip_type.value,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat()
        })
        
        research_data = self._parse_json_from_response(response)
        return research_data


class AccommodationAgent(BaseAgent):
    """Agent responsible for finding and recommending accommodations."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an accommodation specialist. Find the best lodging options based on the trip requirements.

Consider:
- Budget constraints
- Number of travelers
- Trip type and preferences
- Location convenience
- Amenities needed
- Safety and reviews

Return a JSON array of accommodation options:
[
    {
        "name": "accommodation name",
        "type": "hotel/hostel/apartment/etc",
        "location": "specific location/area",
        "price_per_night": "estimated price range",
        "rating": 4.5,
        "amenities": ["wifi", "breakfast", "gym", "etc"],
        "booking_url": "booking website or null",
        "description": "why this is recommended"
    }
]

Provide 3-5 options across different price points within the specified budget range."""),
            ("human", """Find accommodations for:
Destination: {destination}
Dates: {start_date} to {end_date}
Travelers: {travelers}
Budget: {budget}
Trip type: {trip_type}
Preferences: {preferences}
Special requirements: {mobility_requirements}

Research data context: {research_context}""")
        ])

    def find_accommodations(self, state: AgentState) -> List[Accommodation]:
        """Find suitable accommodations based on trip requirements."""
        request = state.trip_request
        research_context = json.dumps(state.destination_research or {}, indent=2)
        
        chain = self.prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "destination": request.destination,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat(),
            "travelers": request.travelers,
            "budget": request.budget.value,
            "trip_type": request.trip_type.value,
            "preferences": ", ".join(request.preferences),
            "mobility_requirements": request.mobility_requirements or "None",
            "research_context": research_context
        })
        
        accommodations_data = self._parse_json_from_response(response)
        
        accommodations = []
        if isinstance(accommodations_data, list):
            for acc_data in accommodations_data:
                try:
                    accommodation = Accommodation(**acc_data)
                    accommodations.append(accommodation)
                except Exception as e:
                    print(f"Error parsing accommodation: {e}")
                    continue
        
        return accommodations


class ActivityAgent(BaseAgent):
    """Agent responsible for finding activities and attractions."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an activity and attraction specialist. Find engaging activities based on trip requirements.

Consider:
- Trip type and traveler interests
- Budget constraints
- Duration and scheduling
- Weather and season
- Local events and festivals
- Accessibility requirements

Return a JSON array of activities:
[
    {
        "name": "activity name",
        "description": "detailed description",
        "duration": "estimated time needed",
        "cost_estimate": "price range or 'free'",
        "location": "specific location",
        "category": "sightseeing/adventure/cultural/food/etc",
        "booking_required": true/false,
        "booking_url": "url or null",
        "best_time": "morning/afternoon/evening/anytime"
    }
]

Provide 10-15 diverse activities covering different categories and time slots."""),
            ("human", """Find activities for:
Destination: {destination}
Dates: {start_date} to {end_date}
Travelers: {travelers}
Budget: {budget}
Trip type: {trip_type}
Preferences: {preferences}
Dietary restrictions: {dietary_restrictions}

Research data context: {research_context}""")
        ])

    def find_activities(self, state: AgentState) -> List[Activity]:
        """Find suitable activities based on trip requirements."""
        request = state.trip_request
        research_context = json.dumps(state.destination_research or {}, indent=2)
        
        chain = self.prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "destination": request.destination,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat(),
            "travelers": request.travelers,
            "budget": request.budget.value,
            "trip_type": request.trip_type.value,
            "preferences": ", ".join(request.preferences),
            "dietary_restrictions": ", ".join(request.dietary_restrictions),
            "research_context": research_context
        })
        
        activities_data = self._parse_json_from_response(response)
        
        activities = []
        if isinstance(activities_data, list):
            for act_data in activities_data:
                try:
                    activity = Activity(**act_data)
                    activities.append(activity)
                except Exception as e:
                    print(f"Error parsing activity: {e}")
                    continue
        
        return activities


class ItineraryAgent(BaseAgent):
    """Agent responsible for creating day-by-day itineraries."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an itinerary planning expert. Create a detailed day-by-day schedule that optimizes the trip experience.

Consider:
- Logical flow and geographic proximity
- Time management and realistic scheduling
- Mix of activities (don't overpack days)
- Rest time and meal breaks
- Transportation between locations
- Opening hours and seasonal considerations

Create a balanced itinerary that maximizes enjoyment while being practical.

Return a JSON array of daily itineraries:
[
    {
        "day": 1,
        "date": "YYYY-MM-DD",
        "activities": [
            {
                "name": "activity name",
                "description": "description",
                "duration": "time needed",
                "cost_estimate": "cost",
                "location": "location",
                "category": "category",
                "booking_required": false,
                "booking_url": null,
                "scheduled_time": "09:00"
            }
        ],
        "meals": [
            {
                "type": "breakfast/lunch/dinner",
                "restaurant": "restaurant name",
                "cuisine": "cuisine type",
                "location": "location",
                "estimated_cost": "cost range",
                "time": "12:00"
            }
        ],
        "transportation": [],
        "notes": "any special notes for the day"
    }
]"""),
            ("human", """Create a detailed itinerary for:
Destination: {destination}
Start date: {start_date}
End date: {end_date}
Number of days: {duration}
Travelers: {travelers}
Budget: {budget}
Trip type: {trip_type}

Available accommodations: {accommodations}
Available activities: {activities}
Research context: {research_context}

Create a balanced schedule that includes the best activities, good meal recommendations, and practical logistics.""")
        ])

    def create_itinerary(self, state: AgentState) -> List[DayItinerary]:
        """Create a detailed day-by-day itinerary."""
        request = state.trip_request
        duration = (request.end_date - request.start_date).days + 1
        
        accommodations_json = json.dumps([acc.dict() for acc in state.accommodations], indent=2)
        activities_json = json.dumps([act.dict() for act in state.activities], indent=2)
        research_context = json.dumps(state.destination_research or {}, indent=2)
        
        chain = self.prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "destination": request.destination,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat(),
            "duration": duration,
            "travelers": request.travelers,
            "budget": request.budget.value,
            "trip_type": request.trip_type.value,
            "accommodations": accommodations_json,
            "activities": activities_json,
            "research_context": research_context
        })
        
        itinerary_data = self._parse_json_from_response(response)
        
        itineraries = []
        if isinstance(itinerary_data, list):
            for day_data in itinerary_data:
                try:
                    # Parse activities within the day
                    activities = []
                    for act_data in day_data.get("activities", []):
                        activity = Activity(**act_data)
                        activities.append(activity)
                    
                    day_itinerary = DayItinerary(
                        day=day_data["day"],
                        date=datetime.fromisoformat(day_data["date"]).date(),
                        activities=activities,
                        meals=day_data.get("meals", []),
                        transportation=day_data.get("transportation", []),
                        notes=day_data.get("notes")
                    )
                    itineraries.append(day_itinerary)
                except Exception as e:
                    print(f"Error parsing day itinerary: {e}")
                    continue
        
        return itineraries


class BudgetAgent(BaseAgent):
    """Agent responsible for budget planning and cost estimation."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a budget planning expert. Calculate realistic cost estimates for the entire trip.

Break down costs into categories:
- Accommodation (total for all nights)
- Transportation (flights, local transport, etc.)
- Activities (entrance fees, tours, etc.)
- Meals (breakfast, lunch, dinner for all days)
- Miscellaneous (tips, shopping, emergencies)

Provide realistic estimates based on the destination, budget level, and planned activities.

Return a JSON object:
{
    "accommodation": "total cost range",
    "transportation": "total cost range", 
    "activities": "total cost range",
    "meals": "total cost range",
    "miscellaneous": "total cost range",
    "total_estimate": "total trip cost range",
    "daily_average": "average cost per day",
    "budget_tips": ["money-saving tips"],
    "currency_info": "local currency and exchange tips"
}"""),
            ("human", """Calculate budget for:
Destination: {destination}
Duration: {duration} days
Travelers: {travelers}
Budget level: {budget}
Trip type: {trip_type}

Accommodations: {accommodations}
Planned itinerary: {itinerary}
Research context: {research_context}

Provide realistic cost estimates and money-saving tips.""")
        ])

    def calculate_budget(self, state: AgentState) -> BudgetBreakdown:
        """Calculate comprehensive budget breakdown."""
        request = state.trip_request
        duration = (request.end_date - request.start_date).days + 1
        
        accommodations_json = json.dumps([acc.dict() for acc in state.accommodations], indent=2)
        itinerary_json = json.dumps([day.dict() for day in state.itinerary], indent=2)
        research_context = json.dumps(state.destination_research or {}, indent=2)
        
        chain = self.prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "destination": request.destination,
            "duration": duration,
            "travelers": request.travelers,
            "budget": request.budget.value,
            "trip_type": request.trip_type.value,
            "accommodations": accommodations_json,
            "itinerary": itinerary_json,
            "research_context": research_context
        })
        
        budget_data = self._parse_json_from_response(response)
        
        try:
            budget_breakdown = BudgetBreakdown(
                accommodation=budget_data.get("accommodation"),
                transportation=budget_data.get("transportation"),
                activities=budget_data.get("activities"),
                meals=budget_data.get("meals"),
                miscellaneous=budget_data.get("miscellaneous"),
                total_estimate=budget_data.get("total_estimate")
            )
            return budget_breakdown
        except Exception as e:
            print(f"Error parsing budget breakdown: {e}")
            return BudgetBreakdown()


class TravelTipsAgent(BaseAgent):
    """Agent responsible for providing travel tips and final recommendations."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(model_name)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a travel advisor providing final tips and recommendations.

Provide practical advice including:
- Packing suggestions specific to destination and activities
- Travel safety tips
- Local customs and etiquette
- Emergency contacts and important numbers
- Health and vaccination requirements
- Technology and communication tips
- Final recommendations to enhance the trip

Return a JSON object:
{
    "packing_suggestions": ["item1", "item2", ...],
    "travel_tips": ["tip1", "tip2", ...],
    "safety_advice": ["advice1", "advice2", ...],
    "emergency_contacts": [
        {"type": "Emergency Services", "number": "911", "notes": "General emergency"},
        {"type": "Tourist Police", "number": "+country-code-number", "notes": "For tourist assistance"}
    ],
    "health_requirements": ["requirement1", "requirement2", ...],
    "cultural_etiquette": ["etiquette1", "etiquette2", ...],
    "final_recommendations": ["recommendation1", "recommendation2", ...]
}"""),
            ("human", """Provide travel tips for:
Destination: {destination}
Trip dates: {start_date} to {end_date}
Travelers: {travelers}
Trip type: {trip_type}
Planned activities: {activities_summary}

Research context: {research_context}

Focus on practical, actionable advice that will enhance the travel experience.""")
        ])

    def generate_tips(self, state: AgentState) -> Dict[str, Any]:
        """Generate comprehensive travel tips and recommendations."""
        request = state.trip_request
        
        # Summarize planned activities
        activities_summary = [f"{act.name} ({act.category})" for act in state.activities[:10]]
        
        research_context = json.dumps(state.destination_research or {}, indent=2)
        
        chain = self.prompt | self.llm | self.output_parser
        
        response = chain.invoke({
            "destination": request.destination,
            "start_date": request.start_date.isoformat(),
            "end_date": request.end_date.isoformat(),
            "travelers": request.travelers,
            "trip_type": request.trip_type.value,
            "activities_summary": ", ".join(activities_summary),
            "research_context": research_context
        })
        
        tips_data = self._parse_json_from_response(response)
        return tips_data