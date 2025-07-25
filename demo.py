#!/usr/bin/env python3
"""
Demo script for the Trip Planner Agent using LangGraph.
This shows a quick example of how the system works.
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
    """Demonstrate the trip planner with a sample request."""
    
    print("🌍 Trip Planner Agent Demo using LangGraph")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  No OpenAI API key found. This demo will show the structure without API calls.")
        print("To get full functionality, add OPENAI_API_KEY to your .env file.")
        print()
    
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
        preferences=["temples", "food tours", "traditional culture", "shopping"],
        dietary_restrictions=["vegetarian-friendly options"]
    )
    
    print(f"📋 Sample Trip Request:")
    print(f"   Destination: {trip_request.destination}")
    print(f"   Dates: {trip_request.start_date} to {trip_request.end_date}")
    print(f"   Duration: {trip_request.duration_days} days")
    print(f"   Budget: {trip_request.budget.value}")
    print(f"   Type: {trip_request.trip_type.value}")
    print(f"   Travelers: {trip_request.travelers}")
    print(f"   Preferences: {', '.join(trip_request.preferences)}")
    print()
    
    # Create the trip planner
    print("🤖 Initializing LangGraph Trip Planner...")
    planner = create_trip_planner()
    print("✅ Trip planner created with 6 specialized agents:")
    print("   • Research Agent - Destination information")
    print("   • Accommodation Agent - Hotels and lodging")
    print("   • Activity Agent - Things to do and see")
    print("   • Itinerary Agent - Day-by-day planning")
    print("   • Budget Agent - Cost calculations")
    print("   • Travel Tips Agent - Practical advice")
    print()
    
    if os.getenv("OPENAI_API_KEY"):
        print("🚀 Running trip planning workflow...")
        print("This may take 1-2 minutes as agents collaborate...")
        
        try:
            # Run the planning workflow
            result = planner.plan_trip(trip_request)
            
            if result and result.get('trip_plan'):
                print("✅ Trip planning completed!")
                print()
                
                # Display the formatted trip plan
                formatted_plan = format_trip_plan(result['trip_plan'])
                print(formatted_plan)
                
                # Save to file
                filename = f"trip_plan_{trip_request.destination.replace(', ', '_').replace(' ', '_').lower()}_{start_date}.json"
                with open(filename, 'w') as f:
                    import json
                    f.write(json.dumps(result['trip_plan'].dict(), indent=2, default=str))
                print(f"💾 Trip plan saved to: {filename}")
                
            else:
                print("❌ Trip planning failed. Check your API key and try again.")
                
        except Exception as e:
            print(f"❌ Error during trip planning: {str(e)}")
            print("This might be due to API rate limits or network issues.")
    
    else:
        print("💡 To see the full trip planning in action:")
        print("   1. Get an OpenAI API key from https://platform.openai.com/")
        print("   2. Copy .env.example to .env")
        print("   3. Add your API key: OPENAI_API_KEY=your_key_here")
        print("   4. Run: python demo.py")
    
    print()
    print("🎯 Key Features of this LangGraph Trip Planner:")
    print("   • Multi-agent collaboration using LangGraph workflows")
    print("   • Comprehensive trip planning (accommodation, activities, budget)")
    print("   • Flexible input options (budget, trip type, preferences)")
    print("   • Rich output formatting and export capabilities")
    print("   • Modular architecture - easy to extend with new agents")
    print()
    print("📚 See README.md for full documentation and examples.")

if __name__ == "__main__":
    demo_trip_planner()