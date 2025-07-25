#!/usr/bin/env python3
"""
Demo script for the Trip Planner Agent using LangGraph.
This demonstrates the complete workflow without requiring user input.
"""

import os
from datetime import date, timedelta
from dotenv import load_dotenv

from trip_planner import (
    TripRequest, TripType, BudgetRange,
    create_trip_planner
)
from trip_planner.utils import format_trip_plan, print_planning_status


def run_demo():
    """Run a demonstration of the trip planner."""
    print("🌍 Trip Planner Agent Demo - Using LangGraph")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Demo Mode: No OpenAI API key found.")
        print("This demo will show the structure without making actual API calls.")
        print("To run with real AI agents, set OPENAI_API_KEY in your .env file.\n")
        demo_mode = True
    else:
        print("🤖 AI Mode: OpenAI API key found. Running with real AI agents.\n")
        demo_mode = False
    
    # Create a sample trip request
    start_date = date.today() + timedelta(days=30)
    end_date = start_date + timedelta(days=6)
    
    trip_request = TripRequest(
        destination="Tokyo, Japan",
        start_date=start_date,
        end_date=end_date,
        budget=BudgetRange.MODERATE,
        trip_type=TripType.CULTURAL,
        travelers=2,
        preferences=["temples", "food tours", "traditional culture", "gardens"],
        dietary_restrictions=["vegetarian"]
    )
    
    print("📋 Trip Request Details:")
    print(f"   🎯 Destination: {trip_request.destination}")
    print(f"   📅 Dates: {trip_request.start_date} to {trip_request.end_date}")
    print(f"   👥 Travelers: {trip_request.travelers}")
    print(f"   💰 Budget: {trip_request.budget.value}")
    print(f"   🎨 Trip Type: {trip_request.trip_type.value}")
    print(f"   ❤️  Preferences: {', '.join(trip_request.preferences)}")
    print(f"   🥗 Dietary: {', '.join(trip_request.dietary_restrictions)}")
    print()
    
    if demo_mode:
        print("📝 Demo Mode - Showing workflow structure:")
        print("   1. 🔍 Research Agent - Analyzes destination")
        print("   2. 🏨 Accommodation Agent - Finds hotels/accommodations")
        print("   3. 🎯 Activity Agent - Discovers activities and attractions")
        print("   4. 📅 Itinerary Agent - Creates daily schedules")
        print("   5. 💰 Budget Agent - Calculates costs and budget breakdown")
        print("   6. 💡 Travel Tips Agent - Provides practical advice")
        print()
        print("🔧 LangGraph Workflow:")
        print("   → All agents work together in a coordinated state machine")
        print("   → Each agent contributes specialized knowledge")
        print("   → Final output combines all agent results into comprehensive plan")
        print()
        print("To see this in action with real AI, add your OpenAI API key to .env file!")
        return
    
    # Create and run the trip planner
    try:
        print("🚀 Initializing LangGraph Trip Planner...")
        planner = create_trip_planner()
        
        print("🤖 Running AI agents...")
        print_planning_status("Starting trip planning process")
        
        # Run the planning process
        result = planner.invoke({"trip_request": trip_request})
        
        if result and result.get("trip_plan"):
            trip_plan = result["trip_plan"]
            print("\n" + "=" * 60)
            print("🎉 TRIP PLAN GENERATED SUCCESSFULLY!")
            print("=" * 60)
            print(format_trip_plan(trip_plan))
            
            # Save the plan
            filename = f"trip_plan_{trip_request.destination.replace(', ', '_').replace(' ', '_').lower()}_{trip_request.start_date}.json"
            print(f"\n💾 Trip plan saved to: {filename}")
            
        else:
            print("❌ Failed to generate trip plan. Please check your API key and try again.")
            
    except Exception as e:
        print(f"❌ Error during trip planning: {str(e)}")
        print("Please check your API key and internet connection.")


if __name__ == "__main__":
    run_demo()