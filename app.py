#!/usr/bin/env python3
"""
Trip Planner Web Application
A beautiful web frontend for the LangGraph trip planner.
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import date, timedelta, datetime
from dotenv import load_dotenv

# Import our trip planner components
try:
    from trip_planner import TripRequest, TripType, BudgetRange, create_trip_planner
    from trip_planner.utils import format_trip_plan
    TRIP_PLANNER_AVAILABLE = True
except ImportError:
    TRIP_PLANNER_AVAILABLE = False

app = Flask(__name__)
load_dotenv()

# Mock data for demo purposes
def create_mock_trip_plan():
    """Create a mock trip plan for demo purposes."""
    return {
        "destination": "Milan, Italy",
        "start_date": "2025-08-24",
        "end_date": "2025-08-28",
        "duration_days": 5,
        "accommodations": [
            {
                "name": "Hotel Spadari Al Duomo",
                "type": "Boutique Hotel",
                "location": "City Center - Near Duomo",
                "price_per_night": "€145",
                "rating": "4.5/5",
                "amenities": ["Free WiFi", "Breakfast", "Air Conditioning", "Fitness Center"]
            }
        ],
        "daily_itineraries": [
            {
                "day": 1,
                "date": "Sunday, August 24",
                "theme": "Arrival & Historic Center",
                "activities": [
                    {"time": "10:00", "activity": "Arrival & Hotel Check-in", "location": "Hotel Spadari Al Duomo"},
                    {"time": "11:30", "activity": "Duomo di Milano Visit", "location": "Piazza del Duomo", "cost": "€15"},
                    {"time": "14:00", "activity": "Lunch at Luini Panzerotti", "location": "Via Santa Radegonda", "cost": "€12"},
                    {"time": "17:30", "activity": "Aperitivo at Camparino", "location": "Galleria Vittorio Emanuele II", "cost": "€18"}
                ]
            },
            {
                "day": 2,
                "date": "Monday, August 25",
                "theme": "Fashion & Design District",
                "activities": [
                    {"time": "10:30", "activity": "Quadrilatero della Moda Shopping", "location": "Fashion District", "cost": "€200"},
                    {"time": "15:30", "activity": "Pinacoteca di Brera", "location": "Brera District", "cost": "€15"},
                    {"time": "20:00", "activity": "Dinner at Osteria di Brera", "location": "Via Brera", "cost": "€55"}
                ]
            }
        ],
        "budget_breakdown": {
            "accommodation": {"total": "€580", "per_night": "€145"},
            "meals": {"total": "€520", "per_day": "€52"},
            "activities": {"total": "€180"},
            "transportation": {"total": "€140"},
            "total_per_person": "€860",
            "total_for_trip": "€1720"
        },
        "travel_tips": [
            "🕐 Best times for aperitivo: 6:00-8:00 PM - it's a Milan tradition!",
            "👗 Dress code: Milan is fashion-forward, dress stylishly",
            "🚇 Get a Milan metro day pass (€7) for unlimited public transport",
            "🍝 Dining tip: Lunch 12:30-2:30 PM, dinner after 7:30 PM"
        ]
    }

@app.route('/')
def index():
    """Main page with trip planning form."""
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan_trip():
    """Handle trip planning request."""
    try:
        data = request.get_json()
        
        # Extract form data
        destination = data.get('destination', 'Milan, Italy')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        budget = data.get('budget', 'moderate')
        trip_type = data.get('trip_type', 'cultural')
        travelers = int(data.get('travelers', 2))
        preferences = data.get('preferences', [])
        dietary_restrictions = data.get('dietary_restrictions', [])
        
        # Check if we have OpenAI API key
        has_api_key = bool(os.getenv("OPENAI_API_KEY"))
        
        if has_api_key and TRIP_PLANNER_AVAILABLE:
            # Use real trip planner
            trip_request = TripRequest(
                destination=destination,
                start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
                end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
                budget=BudgetRange(budget),
                trip_type=TripType(trip_type),
                travelers=travelers,
                preferences=preferences,
                dietary_restrictions=dietary_restrictions
            )
            
            planner = create_trip_planner()
            result = planner.plan_trip(trip_request)
            
            if result and result.get('trip_plan'):
                trip_plan = result['trip_plan']
                # Convert to dict for JSON serialization
                plan_data = {
                    "destination": trip_plan.destination,
                    "start_date": str(trip_plan.start_date),
                    "end_date": str(trip_plan.end_date),
                    "duration_days": trip_plan.duration_days,
                    "accommodations": [acc.dict() for acc in trip_plan.accommodations],
                    "daily_itineraries": [day.dict() for day in trip_plan.daily_itineraries],
                    "budget_breakdown": trip_plan.budget_breakdown.dict(),
                    "travel_tips": trip_plan.travel_tips
                }
                return jsonify({"success": True, "trip_plan": plan_data})
            else:
                return jsonify({"success": False, "error": "Failed to generate trip plan"})
        else:
            # Use mock data for demo
            mock_plan = create_mock_trip_plan()
            # Customize mock data based on input
            mock_plan["destination"] = destination
            mock_plan["start_date"] = start_date
            mock_plan["end_date"] = end_date
            
            return jsonify({"success": True, "trip_plan": mock_plan, "demo_mode": True})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/demo')
def demo():
    """Demo page showing a pre-generated trip plan."""
    mock_plan = create_mock_trip_plan()
    return render_template('trip_plan.html', trip_plan=mock_plan, demo_mode=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)