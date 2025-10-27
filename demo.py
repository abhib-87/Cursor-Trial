#!/usr/bin/env python3
"""
Demo script for the Trip Planner Agent using LangGraph.
This demonstrates the trip planner with a realistic example.
"""

import os
from datetime import date, timedelta
from dotenv import load_dotenv

from trip_planner import (
    TripRequest, TripType, BudgetRange,
    create_trip_planner
)
from trip_planner.utils import format_trip_plan

def demo_trip_planner():
    """Demonstrate the trip planner with a sample Tokyo trip."""
    
    print("🌟 Trip Planner Agent Demo using LangGraph")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Demo Mode: No API key found.")
        print("Set OPENAI_API_KEY in .env file to run with real AI agents.")
        print("\nFor now, showing the structure and workflow...")
        
        # Show the workflow structure
        planner = create_trip_planner()
        print(f"\n🤖 Created trip planner with {len(planner.graph.nodes)} nodes:")
        for node in planner.graph.nodes:
            print(f"   • {node}")
        
        print("\n📋 Sample trip request structure:")
        sample_request = TripRequest(
            destination="Tokyo, Japan",
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=37),
            budget=BudgetRange.MODERATE,
            trip_type=TripType.CULTURAL,
            travelers=2,
            preferences=["temples", "food tours", "cherry blossoms", "traditional culture"],
            dietary_restrictions=["vegetarian options preferred"]
        )
        
        print(f"   Destination: {sample_request.destination}")
        print(f"   Duration: {sample_request.duration_days} days")
        print(f"   Budget: {sample_request.budget}")
        print(f"   Trip Type: {sample_request.trip_type}")
        print(f"   Travelers: {sample_request.travelers}")
        print(f"   Preferences: {', '.join(sample_request.preferences)}")
        
        print("\n🔄 Workflow Process:")
        print("   1. Research Agent → Gathers destination information")
        print("   2. Accommodation Agent → Finds hotels/lodging")
        print("   3. Activity Agent → Discovers attractions and activities")
        print("   4. Itinerary Agent → Creates day-by-day schedule")
        print("   5. Budget Agent → Calculates costs and budget breakdown")
        print("   6. Travel Tips Agent → Provides practical advice")
        
        return
    
    # Create the trip planner
    print("🤖 Initializing LangGraph trip planner...")
    planner = create_trip_planner()
    
    # Create a sample trip request
    print("\n📝 Creating sample trip request for Tokyo...")
    trip_request = TripRequest(
        destination="Tokyo, Japan",
        start_date=date.today() + timedelta(days=30),
        end_date=date.today() + timedelta(days=37),
        budget=BudgetRange.MODERATE,
        trip_type=TripType.CULTURAL,
        travelers=2,
        preferences=["temples", "food tours", "cherry blossoms", "traditional culture"],
        dietary_restrictions=["vegetarian options preferred"]
    )
    
    print(f"   📍 Destination: {trip_request.destination}")
    print(f"   📅 Dates: {trip_request.start_date} to {trip_request.end_date}")
    print(f"   💰 Budget: {trip_request.budget}")
    print(f"   🎯 Type: {trip_request.trip_type}")
    
    # Plan the trip
    print("\n🔄 Running trip planning workflow...")
    print("   This may take a few minutes as agents work together...")
    
    try:
        trip_plan = planner.plan_trip(trip_request)
        
        if trip_plan:
            print("\n✅ Trip planning completed successfully!")
            print(format_trip_plan(trip_plan))
            
            # Save the plan
            filename = f"tokyo_trip_plan_{date.today().strftime('%Y%m%d')}.json"
            print(f"\n💾 Saving trip plan to {filename}")
            
        else:
            print("\n❌ Trip planning failed. Please check your API key and try again.")
            
    except Exception as e:
        print(f"\n❌ Error during trip planning: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    demo_trip_planner()