#!/usr/bin/env python3
"""
Example usage of the Trip Planner Agent using LangGraph.

This script demonstrates how to create a trip request and use the
trip planner to generate a comprehensive travel plan.
"""

import os
from datetime import date, timedelta
from dotenv import load_dotenv

from trip_planner import (
    TripRequest, TripType, BudgetRange,
    create_trip_planner
)
from trip_planner.utils import format_trip_plan, save_trip_plan, print_planning_status


def main():
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        print("Example: OPENAI_API_KEY=your_api_key_here")
        return
    
    print("🌟 Welcome to the Trip Planner Agent!")
    print("This example will create a sample trip plan using LangGraph.\n")
    
    # Create a sample trip request
    start_date = date.today() + timedelta(days=30)
    end_date = start_date + timedelta(days=6)
    
    trip_request = TripRequest(
        destination="Paris, France",
        start_date=start_date,
        end_date=end_date,
        budget=BudgetRange.MODERATE,
        trip_type=TripType.CULTURAL,
        travelers=2,
        preferences=["art", "museums", "cuisine", "architecture"],
        dietary_restrictions=["gluten-free"]
    )
    
    print("📋 Trip Request Details:")
    print(f"   🌍 Destination: {trip_request.destination}")
    print(f"   📅 Dates: {trip_request.start_date} to {trip_request.end_date}")
    print(f"   👥 Travelers: {trip_request.travelers}")
    print(f"   💰 Budget: {trip_request.budget.value}")
    print(f"   🎯 Trip Type: {trip_request.trip_type.value}")
    print(f"   ❤️ Preferences: {', '.join(trip_request.preferences)}")
    print(f"   🚫 Dietary Restrictions: {', '.join(trip_request.dietary_restrictions)}")
    print()
    
    # Create the trip planner
    print("🤖 Initializing Trip Planner with LangGraph...")
    trip_planner = create_trip_planner()
    
    # Plan the trip
    print("🚀 Starting trip planning process...\n")
    final_state = trip_planner.plan_trip(trip_request)
    
    # Print status
    print_planning_status(final_state)
    
    # Display the final plan
    if final_state.final_plan:
        print("\n" + "="*60)
        print("📊 FINAL TRIP PLAN")
        print("="*60)
        formatted_plan = format_trip_plan(final_state.final_plan)
        print(formatted_plan)
        
        # Save the plan to a file
        filename = save_trip_plan(final_state.final_plan)
        print(f"\n💾 Trip plan saved to: {filename}")
        
    else:
        print("\n❌ Failed to generate trip plan.")
        if final_state.errors:
            print("Errors encountered:")
            for error in final_state.errors:
                print(f"  - {error}")


def interactive_example():
    """Interactive example allowing user input."""
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found.")
        return
    
    print("🌟 Interactive Trip Planner")
    print("=" * 40)
    
    # Get user input
    destination = input("🌍 Enter destination: ")
    travelers = int(input("👥 Number of travelers: "))
    
    print("\n💰 Budget options:")
    print("1. Budget")
    print("2. Moderate") 
    print("3. Luxury")
    budget_choice = input("Choose budget (1-3): ")
    budget_map = {"1": BudgetRange.BUDGET, "2": BudgetRange.MODERATE, "3": BudgetRange.LUXURY}
    budget = budget_map.get(budget_choice, BudgetRange.MODERATE)
    
    print("\n🎯 Trip type options:")
    print("1. Leisure")
    print("2. Business")
    print("3. Adventure")
    print("4. Cultural")
    print("5. Romantic")
    print("6. Family")
    trip_choice = input("Choose trip type (1-6): ")
    trip_map = {
        "1": TripType.LEISURE, "2": TripType.BUSINESS, "3": TripType.ADVENTURE,
        "4": TripType.CULTURAL, "5": TripType.ROMANTIC, "6": TripType.FAMILY
    }
    trip_type = trip_map.get(trip_choice, TripType.LEISURE)
    
    # Set dates (30 days from now for 7 days)
    start_date = date.today() + timedelta(days=30)
    end_date = start_date + timedelta(days=6)
    
    preferences = input("\n❤️ Enter preferences (comma-separated): ").split(",")
    preferences = [p.strip() for p in preferences if p.strip()]
    
    dietary = input("🚫 Enter dietary restrictions (comma-separated, or press Enter for none): ").split(",")
    dietary = [d.strip() for d in dietary if d.strip()]
    
    # Create trip request
    trip_request = TripRequest(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        trip_type=trip_type,
        travelers=travelers,
        preferences=preferences,
        dietary_restrictions=dietary
    )
    
    # Plan the trip
    trip_planner = create_trip_planner()
    final_state = trip_planner.plan_trip(trip_request)
    
    # Display results
    if final_state.final_plan:
        formatted_plan = format_trip_plan(final_state.final_plan)
        print("\n" + formatted_plan)
        
        save_choice = input("\n💾 Save trip plan to file? (y/n): ")
        if save_choice.lower() == 'y':
            filename = save_trip_plan(final_state.final_plan)
            print(f"✅ Trip plan saved to: {filename}")
    else:
        print("\n❌ Failed to generate trip plan.")


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run example with sample data")
    print("2. Interactive trip planner")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        main()
    elif choice == "2":
        interactive_example()
    else:
        print("Invalid choice. Running example with sample data.")
        main()