"""
Utility functions for the trip planner.
"""

import json
from typing import Dict, Any
from datetime import datetime, date
from .models import TripPlan, AgentState


def format_trip_plan(trip_plan: TripPlan) -> str:
    """Format a trip plan into a readable string."""
    if not trip_plan:
        return "No trip plan available."
    
    output = []
    output.append("=" * 60)
    output.append(f"🌍 TRIP PLAN: {trip_plan.destination.upper()}")
    output.append("=" * 60)
    output.append(f"📅 Duration: {trip_plan.start_date} to {trip_plan.end_date} ({trip_plan.duration_days} days)")
    output.append("")
    
    # Accommodations
    if trip_plan.accommodations:
        output.append("🏨 ACCOMMODATIONS")
        output.append("-" * 30)
        for i, acc in enumerate(trip_plan.accommodations, 1):
            output.append(f"{i}. {acc.name} ({acc.type})")
            output.append(f"   📍 {acc.location}")
            if acc.price_per_night:
                output.append(f"   💰 {acc.price_per_night}/night")
            if acc.rating:
                output.append(f"   ⭐ {acc.rating}/5")
            if acc.amenities:
                output.append(f"   🎯 Amenities: {', '.join(acc.amenities)}")
            output.append("")
    
    # Daily Itinerary
    if trip_plan.daily_itinerary:
        output.append("📅 DAILY ITINERARY")
        output.append("-" * 30)
        for day in trip_plan.daily_itinerary:
            output.append(f"Day {day.day} - {day.date.strftime('%A, %B %d, %Y')}")
            output.append("~" * 40)
            
            for activity in day.activities:
                output.append(f"🎯 {activity.name}")
                output.append(f"   📍 {activity.location}")
                output.append(f"   ⏱️ {activity.duration}")
                if activity.cost_estimate:
                    output.append(f"   💰 {activity.cost_estimate}")
                output.append(f"   📝 {activity.description}")
                output.append("")
            
            if day.meals:
                output.append("🍽️ Meals:")
                for meal in day.meals:
                    meal_type = meal.get('type', 'meal').title()
                    restaurant = meal.get('restaurant', 'TBD')
                    output.append(f"   {meal_type}: {restaurant}")
                output.append("")
            
            if day.notes:
                output.append(f"📝 Notes: {day.notes}")
                output.append("")
            
            output.append("")
    
    # Budget Breakdown
    if trip_plan.budget_breakdown:
        output.append("💰 BUDGET BREAKDOWN")
        output.append("-" * 30)
        budget = trip_plan.budget_breakdown
        if budget.accommodation:
            output.append(f"🏨 Accommodation: {budget.accommodation}")
        if budget.transportation:
            output.append(f"🚗 Transportation: {budget.transportation}")
        if budget.activities:
            output.append(f"🎯 Activities: {budget.activities}")
        if budget.meals:
            output.append(f"🍽️ Meals: {budget.meals}")
        if budget.miscellaneous:
            output.append(f"🛍️ Miscellaneous: {budget.miscellaneous}")
        if budget.total_estimate:
            output.append("-" * 20)
            output.append(f"💵 TOTAL ESTIMATE: {budget.total_estimate}")
        output.append("")
    
    # Travel Tips
    if trip_plan.travel_tips:
        output.append("💡 TRAVEL TIPS")
        output.append("-" * 30)
        for tip in trip_plan.travel_tips:
            output.append(f"• {tip}")
        output.append("")
    
    # Packing Suggestions
    if trip_plan.packing_suggestions:
        output.append("🎒 PACKING SUGGESTIONS")
        output.append("-" * 30)
        for item in trip_plan.packing_suggestions:
            output.append(f"• {item}")
        output.append("")
    
    # Emergency Contacts
    if trip_plan.emergency_contacts:
        output.append("🚨 EMERGENCY CONTACTS")
        output.append("-" * 30)
        for contact in trip_plan.emergency_contacts:
            contact_type = contact.get('type', 'Contact')
            number = contact.get('number', 'N/A')
            notes = contact.get('notes', '')
            output.append(f"• {contact_type}: {number}")
            if notes:
                output.append(f"  {notes}")
        output.append("")
    
    output.append("=" * 60)
    output.append("🎉 Have a wonderful trip!")
    output.append("=" * 60)
    
    return "\n".join(output)


def save_trip_plan(trip_plan: TripPlan, filename: str = None) -> str:
    """Save a trip plan to a JSON file."""
    if not filename:
        safe_destination = "".join(c for c in trip_plan.destination if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_destination = safe_destination.replace(' ', '_')
        filename = f"trip_plan_{safe_destination}_{trip_plan.start_date}.json"
    
    # Convert to dict for JSON serialization
    plan_dict = trip_plan.dict()
    
    # Convert dates to strings
    plan_dict['start_date'] = trip_plan.start_date.isoformat()
    plan_dict['end_date'] = trip_plan.end_date.isoformat()
    
    for day in plan_dict['daily_itinerary']:
        day['date'] = datetime.fromisoformat(day['date']).date().isoformat()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(plan_dict, f, indent=2, ensure_ascii=False)
    
    return filename


def load_trip_plan(filename: str) -> TripPlan:
    """Load a trip plan from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        plan_dict = json.load(f)
    
    # Convert date strings back to date objects
    plan_dict['start_date'] = datetime.fromisoformat(plan_dict['start_date']).date()
    plan_dict['end_date'] = datetime.fromisoformat(plan_dict['end_date']).date()
    
    for day in plan_dict['daily_itinerary']:
        day['date'] = datetime.fromisoformat(day['date']).date()
    
    return TripPlan(**plan_dict)


def print_planning_status(state: AgentState):
    """Print the current status of trip planning."""
    print(f"\n📊 Planning Status: {state.current_step}")
    print(f"🎯 Destination: {state.trip_request.destination}")
    
    if state.destination_research:
        print("✅ Research completed")
    
    if state.accommodations:
        print(f"✅ Found {len(state.accommodations)} accommodations")
    
    if state.activities:
        print(f"✅ Found {len(state.activities)} activities")
    
    if state.itinerary:
        print(f"✅ Created {len(state.itinerary)} day itinerary")
    
    if state.budget_breakdown:
        print("✅ Budget calculated")
    
    if state.final_plan:
        print("✅ Trip plan finalized")
    
    if state.errors:
        print(f"⚠️ {len(state.errors)} errors occurred")
        for error in state.errors:
            print(f"  - {error}")


def create_sample_trip_request():
    """Create a sample trip request for testing."""
    from datetime import date, timedelta
    from .models import TripRequest, TripType, BudgetRange
    
    start_date = date.today() + timedelta(days=30)
    end_date = start_date + timedelta(days=6)
    
    return TripRequest(
        destination="Tokyo, Japan",
        start_date=start_date,
        end_date=end_date,
        budget=BudgetRange.MODERATE,
        trip_type=TripType.CULTURAL,
        travelers=2,
        preferences=["temples", "food", "technology", "gardens"],
        dietary_restrictions=["vegetarian"]
    )