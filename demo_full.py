#!/usr/bin/env python3
"""
Complete Trip Planner Demo - Simulated End-to-End Experience
This shows exactly what the application looks like with mock AI responses.
"""

import os
import json
from datetime import date, timedelta
from typing import List, Dict, Any

# Mock the trip planner components
class MockTripRequest:
    def __init__(self, destination, start_date, end_date, budget, trip_type, travelers, preferences, dietary_restrictions=None):
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.trip_type = trip_type
        self.travelers = travelers
        self.preferences = preferences
        self.dietary_restrictions = dietary_restrictions or []
        self.duration_days = (end_date - start_date).days + 1

class MockTripPlan:
    def __init__(self, destination, start_date, end_date, accommodations, daily_itineraries, budget_breakdown, travel_tips):
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.duration_days = (end_date - start_date).days + 1
        self.accommodations = accommodations
        self.daily_itineraries = daily_itineraries
        self.budget_breakdown = budget_breakdown
        self.travel_tips = travel_tips

def simulate_trip_planning(trip_request):
    """Simulate the complete trip planning process with realistic outputs."""
    
    print("🚀 Starting LangGraph Trip Planning Workflow...")
    print("=" * 60)
    
    # Simulate Research Agent
    print("🔍 Research Agent - Analyzing destination...")
    print("   ✓ Gathering climate and weather information")
    print("   ✓ Researching local culture and customs")
    print("   ✓ Finding top attractions and landmarks")
    print("   ✓ Analyzing transportation options")
    print("   ✓ Checking visa requirements and travel advisories")
    print()
    
    # Simulate Accommodation Agent
    print("🏨 Accommodation Agent - Finding perfect stays...")
    print("   ✓ Searching hotels in central locations")
    print("   ✓ Checking availability for your dates")
    print("   ✓ Comparing prices and amenities")
    print("   ✓ Reading guest reviews and ratings")
    print("   ✓ Filtering by budget and preferences")
    print()
    
    # Simulate Activity Agent
    print("🎯 Activity Agent - Discovering experiences...")
    print("   ✓ Finding must-see attractions")
    print("   ✓ Discovering local experiences")
    print("   ✓ Checking opening hours and ticket prices")
    print("   ✓ Finding restaurants matching dietary needs")
    print("   ✓ Locating shopping and entertainment")
    print()
    
    # Simulate Itinerary Agent
    print("📅 Itinerary Agent - Creating daily schedules...")
    print("   ✓ Optimizing travel routes")
    print("   ✓ Balancing activities and rest time")
    print("   ✓ Considering opening hours and crowds")
    print("   ✓ Adding buffer time for meals and transport")
    print("   ✓ Creating logical daily flows")
    print()
    
    # Simulate Budget Agent
    print("💰 Budget Agent - Calculating costs...")
    print("   ✓ Estimating accommodation costs")
    print("   ✓ Calculating meal and dining expenses")
    print("   ✓ Adding activity and attraction fees")
    print("   ✓ Including transportation costs")
    print("   ✓ Adding contingency and tips")
    print()
    
    # Simulate Travel Tips Agent
    print("💡 Travel Tips Agent - Providing insights...")
    print("   ✓ Sharing local customs and etiquette")
    print("   ✓ Providing packing recommendations")
    print("   ✓ Suggesting useful apps and tools")
    print("   ✓ Adding safety and health tips")
    print("   ✓ Including language basics")
    print()
    
    print("🎉 Trip planning completed! Generating comprehensive plan...")
    print()
    
    # Create mock trip plan based on destination
    if "Milan" in trip_request.destination:
        return create_milan_trip_plan(trip_request)
    elif "Tokyo" in trip_request.destination:
        return create_tokyo_trip_plan(trip_request)
    else:
        return create_generic_trip_plan(trip_request)

def create_milan_trip_plan(trip_request):
    """Create a realistic Milan trip plan."""
    
    accommodations = [
        {
            "name": "Hotel Spadari Al Duomo",
            "type": "Boutique Hotel",
            "location": "City Center - Near Duomo",
            "price_per_night": "€145",
            "rating": "4.5/5",
            "amenities": ["Free WiFi", "Breakfast", "Air Conditioning", "Fitness Center"],
            "description": "Stylish boutique hotel steps from the Duomo with contemporary design"
        }
    ]
    
    daily_itineraries = [
        {
            "day": 1,
            "date": trip_request.start_date,
            "theme": "Arrival & Historic Center",
            "activities": [
                {"time": "10:00", "activity": "Arrival & Hotel Check-in", "location": "Hotel Spadari Al Duomo", "duration": "1 hour"},
                {"time": "11:30", "activity": "Duomo di Milano Visit", "location": "Piazza del Duomo", "duration": "2 hours", "cost": "€15"},
                {"time": "14:00", "activity": "Lunch at Luini Panzerotti", "location": "Via Santa Radegonda", "duration": "1 hour", "cost": "€12"},
                {"time": "15:30", "activity": "La Scala Theatre Tour", "location": "Teatro alla Scala", "duration": "1.5 hours", "cost": "€9"},
                {"time": "17:30", "activity": "Aperitivo at Camparino", "location": "Galleria Vittorio Emanuele II", "duration": "1.5 hours", "cost": "€18"},
                {"time": "19:30", "activity": "Dinner at Trattoria Milanese", "location": "Via Santa Marta", "duration": "2 hours", "cost": "€45"}
            ]
        },
        {
            "day": 2,
            "date": trip_request.start_date + timedelta(days=1),
            "theme": "Fashion & Design District",
            "activities": [
                {"time": "09:00", "activity": "Breakfast at hotel", "location": "Hotel", "duration": "1 hour", "cost": "€20"},
                {"time": "10:30", "activity": "Quadrilatero della Moda Shopping", "location": "Fashion District", "duration": "3 hours", "cost": "€200"},
                {"time": "14:00", "activity": "Lunch at Peck Italian Bar", "location": "Via Spadari", "duration": "1 hour", "cost": "€35"},
                {"time": "15:30", "activity": "Pinacoteca di Brera", "location": "Brera District", "duration": "2 hours", "cost": "€15"},
                {"time": "18:00", "activity": "Explore Brera District", "location": "Brera", "duration": "2 hours", "cost": "€0"},
                {"time": "20:00", "activity": "Dinner at Osteria di Brera", "location": "Via Brera", "duration": "2 hours", "cost": "€55"}
            ]
        },
        {
            "day": 3,
            "date": trip_request.start_date + timedelta(days=2),
            "theme": "Art, Culture & Navigli",
            "activities": [
                {"time": "09:00", "activity": "Breakfast at Pavé", "location": "Via Felice Casati", "duration": "1 hour", "cost": "€15"},
                {"time": "10:30", "activity": "Castello Sforzesco", "location": "Parco Sempione", "duration": "2.5 hours", "cost": "€10"},
                {"time": "13:30", "activity": "Lunch at Dry Milano", "location": "Via Solferino", "duration": "1 hour", "cost": "€30"},
                {"time": "15:00", "activity": "Modern Art at PAC", "location": "Via Palestro", "duration": "2 hours", "cost": "€12"},
                {"time": "17:30", "activity": "Navigli District Walk", "location": "Navigli Canals", "duration": "2 hours", "cost": "€0"},
                {"time": "19:30", "activity": "Aperitivo at Mag Cafè", "location": "Navigli", "duration": "1.5 hours", "cost": "€20"},
                {"time": "21:00", "activity": "Dinner at El Brellin", "location": "Navigli", "duration": "2 hours", "cost": "€50"}
            ]
        },
        {
            "day": 4,
            "date": trip_request.start_date + timedelta(days=3),
            "theme": "Lake Como Day Trip",
            "activities": [
                {"time": "08:00", "activity": "Early breakfast & departure", "location": "Hotel", "duration": "1 hour", "cost": "€15"},
                {"time": "09:30", "activity": "Train to Como", "location": "Milano Centrale", "duration": "1 hour", "cost": "€12"},
                {"time": "11:00", "activity": "Como Cathedral & Historic Center", "location": "Como", "duration": "2 hours", "cost": "€5"},
                {"time": "13:30", "activity": "Lunch with lake view", "location": "Como Lakefront", "duration": "1.5 hours", "cost": "€40"},
                {"time": "15:00", "activity": "Boat trip on Lake Como", "location": "Lake Como", "duration": "2 hours", "cost": "€25"},
                {"time": "17:30", "activity": "Bellagio village visit", "location": "Bellagio", "duration": "2 hours", "cost": "€0"},
                {"time": "20:00", "activity": "Return to Milan", "location": "Train", "duration": "1 hour", "cost": "€12"},
                {"time": "21:30", "activity": "Late dinner in Milan", "location": "Near hotel", "duration": "1.5 hours", "cost": "€35"}
            ]
        },
        {
            "day": 5,
            "date": trip_request.start_date + timedelta(days=4),
            "theme": "Final Shopping & Departure",
            "activities": [
                {"time": "09:00", "activity": "Breakfast & hotel checkout", "location": "Hotel", "duration": "1 hour", "cost": "€20"},
                {"time": "10:30", "activity": "Last-minute shopping", "location": "Corso Buenos Aires", "duration": "2 hours", "cost": "€100"},
                {"time": "13:00", "activity": "Farewell lunch", "location": "Ristorante Cracco", "duration": "2 hours", "cost": "€80"},
                {"time": "15:30", "activity": "Departure to airport", "location": "Malpensa Airport", "duration": "1 hour", "cost": "€25"}
            ]
        }
    ]
    
    budget_breakdown = {
        "accommodation": {"total": "€580", "per_night": "€145", "nights": 4},
        "meals": {"total": "€520", "per_person_per_day": "€52", "days": 5},
        "activities": {"total": "€180", "major_attractions": "€86", "misc": "€94"},
        "transportation": {"total": "€140", "local": "€90", "como_trip": "€50"},
        "shopping": {"total": "€300", "fashion": "€200", "souvenirs": "€100"},
        "total_per_person": "€860",
        "total_for_trip": "€1720"
    }
    
    travel_tips = [
        "🕐 Best times for aperitivo: 6:00-8:00 PM - it's a Milan tradition!",
        "👗 Dress code: Milan is fashion-forward, dress stylishly especially for dinner",
        "🚇 Get a Milan metro day pass (€7) for unlimited public transport",
        "🍝 Dining tip: Lunch is typically 12:30-2:30 PM, dinner after 7:30 PM",
        "💳 Most places accept cards, but carry some cash for small cafes",
        "🛍️ Fashion week seasons: February/March and September/October",
        "🥖 Try local specialties: risotto alla milanese, cotoletta, panettone",
        "📱 Download ATM Milano app for public transport routes and times",
        "🚶‍♀️ Milan is very walkable, especially the city center",
        "☂️ Weather: Pack layers and an umbrella - Milan weather can be unpredictable"
    ]
    
    return MockTripPlan(
        destination=trip_request.destination,
        start_date=trip_request.start_date,
        end_date=trip_request.end_date,
        accommodations=accommodations,
        daily_itineraries=daily_itineraries,
        budget_breakdown=budget_breakdown,
        travel_tips=travel_tips
    )

def format_mock_trip_plan(trip_plan):
    """Format the mock trip plan into a beautiful display."""
    output = []
    output.append("=" * 80)
    output.append(f"🌍 COMPREHENSIVE TRIP PLAN: {trip_plan.destination.upper()}")
    output.append("=" * 80)
    output.append(f"📅 Duration: {trip_plan.start_date} to {trip_plan.end_date} ({trip_plan.duration_days} days)")
    output.append("")
    
    # Accommodations
    output.append("🏨 ACCOMMODATIONS")
    output.append("-" * 40)
    for acc in trip_plan.accommodations:
        output.append(f"🏨 {acc['name']} ({acc['type']})")
        output.append(f"   📍 Location: {acc['location']}")
        output.append(f"   💰 Price: {acc['price_per_night']}/night")
        output.append(f"   ⭐ Rating: {acc['rating']}")
        output.append(f"   🎯 Amenities: {', '.join(acc['amenities'])}")
        output.append(f"   📝 {acc['description']}")
        output.append("")
    
    # Daily Itineraries
    output.append("📅 DAILY ITINERARIES")
    output.append("-" * 40)
    for day_plan in trip_plan.daily_itineraries:
        output.append(f"📅 DAY {day_plan['day']} - {day_plan['date'].strftime('%A, %B %d')} - {day_plan['theme']}")
        output.append("")
        for activity in day_plan['activities']:
            cost_str = f" (€{activity['cost']})" if activity.get('cost') and activity['cost'] != '€0' else ""
            output.append(f"   {activity['time']} - {activity['activity']}{cost_str}")
            output.append(f"             📍 {activity['location']} | ⏱️ {activity['duration']}")
        output.append("")
    
    # Budget Breakdown
    output.append("💰 BUDGET BREAKDOWN")
    output.append("-" * 40)
    budget = trip_plan.budget_breakdown
    output.append(f"🏨 Accommodation: {budget['accommodation']['total']} ({budget['accommodation']['nights']} nights)")
    output.append(f"🍽️ Meals & Dining: {budget['meals']['total']} (avg {budget['meals']['per_person_per_day']}/person/day)")
    output.append(f"🎯 Activities & Attractions: {budget['activities']['total']}")
    output.append(f"🚇 Transportation: {budget['transportation']['total']}")
    output.append(f"🛍️ Shopping & Souvenirs: {budget['shopping']['total']}")
    output.append("")
    output.append(f"💰 TOTAL PER PERSON: {budget['total_per_person']}")
    output.append(f"💰 TOTAL FOR TRIP: {budget['total_for_trip']}")
    output.append("")
    
    # Travel Tips
    output.append("💡 TRAVEL TIPS & RECOMMENDATIONS")
    output.append("-" * 40)
    for tip in trip_plan.travel_tips:
        output.append(f"   {tip}")
    output.append("")
    
    output.append("=" * 80)
    output.append("🎉 Have an amazing trip! Buon viaggio!")
    output.append("=" * 80)
    
    return "\n".join(output)

def main():
    """Run the complete trip planner demo."""
    
    print("🌍 TRIP PLANNER AGENT - COMPLETE DEMO")
    print("Using LangGraph Multi-Agent Architecture")
    print("=" * 80)
    print()
    
    # Create trip request
    start_date = date.today() + timedelta(days=30)
    end_date = start_date + timedelta(days=4)
    
    trip_request = MockTripRequest(
        destination="Milan, Italy",
        start_date=start_date,
        end_date=end_date,
        budget="moderate",
        trip_type="cultural",
        travelers=2,
        preferences=["fashion and design", "Italian cuisine", "art galleries", "historic architecture"],
        dietary_restrictions=["gluten-free options"]
    )
    
    print("📋 TRIP REQUEST SUBMITTED")
    print("-" * 30)
    print(f"🎯 Destination: {trip_request.destination}")
    print(f"📅 Dates: {trip_request.start_date} to {trip_request.end_date}")
    print(f"⏱️ Duration: {trip_request.duration_days} days")
    print(f"👥 Travelers: {trip_request.travelers}")
    print(f"💰 Budget: {trip_request.budget}")
    print(f"🎨 Trip Type: {trip_request.trip_type}")
    print(f"❤️ Preferences: {', '.join(trip_request.preferences)}")
    print(f"🥗 Dietary: {', '.join(trip_request.dietary_restrictions)}")
    print()
    
    # Simulate the planning process
    trip_plan = simulate_trip_planning(trip_request)
    
    # Display the results
    formatted_plan = format_mock_trip_plan(trip_plan)
    print(formatted_plan)
    
    # Save to file
    filename = f"milan_trip_plan_demo_{start_date}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(formatted_plan)
    
    print(f"\n💾 Complete trip plan saved to: {filename}")
    print("\n🎯 This demonstrates the full LangGraph trip planner workflow!")
    print("   • 6 specialized AI agents working together")
    print("   • Comprehensive planning from research to final itinerary")
    print("   • Beautiful formatted output with all details")
    print("   • Ready for real implementation with OpenAI API")

if __name__ == "__main__":
    main()