"""
Trip Planner Agent using LangGraph

A comprehensive trip planning system that uses multiple specialized agents
to research destinations, find accommodations, plan activities, create itineraries,
calculate budgets, and provide travel tips.
"""

from .models import (
    TripRequest, TripType, BudgetRange, Activity, Accommodation,
    Transportation, DayItinerary, BudgetBreakdown, TripPlan, AgentState
)

from .agents import (
    ResearchAgent, AccommodationAgent, ActivityAgent,
    ItineraryAgent, BudgetAgent, TravelTipsAgent
)

from .graph import TripPlannerGraph, create_trip_planner

__version__ = "1.0.0"
__author__ = "Trip Planner Agent"

__all__ = [
    # Models
    "TripRequest", "TripType", "BudgetRange", "Activity", "Accommodation",
    "Transportation", "DayItinerary", "BudgetBreakdown", "TripPlan", "AgentState",
    
    # Agents
    "ResearchAgent", "AccommodationAgent", "ActivityAgent",
    "ItineraryAgent", "BudgetAgent", "TravelTipsAgent",
    
    # Graph
    "TripPlannerGraph", "create_trip_planner"
]