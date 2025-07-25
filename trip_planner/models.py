from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum


class TripType(str, Enum):
    LEISURE = "leisure"
    BUSINESS = "business"
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    ROMANTIC = "romantic"
    FAMILY = "family"


class BudgetRange(str, Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class TripRequest(BaseModel):
    destination: str = Field(..., description="Destination city or country")
    start_date: date = Field(..., description="Trip start date")
    end_date: date = Field(..., description="Trip end date")
    budget: BudgetRange = Field(default=BudgetRange.MODERATE, description="Budget range")
    trip_type: TripType = Field(default=TripType.LEISURE, description="Type of trip")
    travelers: int = Field(default=1, ge=1, description="Number of travelers")
    preferences: Optional[List[str]] = Field(default=[], description="Special preferences or interests")
    dietary_restrictions: Optional[List[str]] = Field(default=[], description="Dietary restrictions")
    mobility_requirements: Optional[str] = Field(default=None, description="Special mobility requirements")


class Activity(BaseModel):
    name: str
    description: str
    duration: str
    cost_estimate: Optional[str] = None
    location: str
    category: str
    booking_required: bool = False
    booking_url: Optional[str] = None


class Accommodation(BaseModel):
    name: str
    type: str  # hotel, hostel, apartment, etc.
    location: str
    price_per_night: Optional[str] = None
    rating: Optional[float] = None
    amenities: List[str] = []
    booking_url: Optional[str] = None


class Transportation(BaseModel):
    mode: str  # flight, train, bus, car rental, etc.
    from_location: str
    to_location: str
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    cost_estimate: Optional[str] = None
    booking_url: Optional[str] = None


class DayItinerary(BaseModel):
    day: int
    date: date
    activities: List[Activity]
    meals: List[Dict[str, Any]] = []
    transportation: List[Transportation] = []
    notes: Optional[str] = None


class BudgetBreakdown(BaseModel):
    accommodation: Optional[str] = None
    transportation: Optional[str] = None
    activities: Optional[str] = None
    meals: Optional[str] = None
    miscellaneous: Optional[str] = None
    total_estimate: Optional[str] = None


class TripPlan(BaseModel):
    destination: str
    start_date: date
    end_date: date
    duration_days: int
    accommodations: List[Accommodation]
    daily_itinerary: List[DayItinerary]
    budget_breakdown: BudgetBreakdown
    travel_tips: List[str] = []
    emergency_contacts: List[Dict[str, str]] = []
    packing_suggestions: List[str] = []


class AgentState(BaseModel):
    trip_request: TripRequest
    destination_research: Optional[Dict[str, Any]] = None
    accommodations: List[Accommodation] = []
    activities: List[Activity] = []
    transportation_options: List[Transportation] = []
    itinerary: List[DayItinerary] = []
    budget_breakdown: Optional[BudgetBreakdown] = None
    final_plan: Optional[TripPlan] = None
    current_step: str = "start"
    errors: List[str] = []
    
    class Config:
        arbitrary_types_allowed = True