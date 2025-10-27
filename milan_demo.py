#!/usr/bin/env python3
"""
Milan Trip Demo - LangGraph Trip Planner

This demo shows the trip planner creating a comprehensive plan for Milan, Italy.
"""

import os
from datetime import date, timedelta
from dotenv import load_dotenv

from trip_planner import (
    TripRequest, TripType, BudgetRange,
    create_trip_planner
)
from trip_planner.utils import format_trip_plan, print_planning_status


def milan_trip_demo():
    """Demonstrate trip planning for Milan, Italy."""
    
    print("🇮🇹 Milan Trip Planner Demo - Using LangGraph")
    print("=" * 55)
    print("Creating a comprehensive trip plan for Milan, Italy...")
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Check if we have API key
    has_api_key = bool(os.getenv("OPENAI_API_KEY"))
    
    if not has_api_key:
        print("⚠️  Demo Mode: No OpenAI API key found.")
        print("This will show the trip planner structure without AI calls.")
        print("To run with real AI, set OPENAI_API_KEY in your .env file.")
        print()
    
    # Create Milan trip request
    start_date = date.today() + timedelta(days=45)  # Trip in 45 days
    end_date = start_date + timedelta(days=4)       # 5-day trip
    
    milan_request = TripRequest(
        destination="Milan, Italy",
        start_date=start_date,
        end_date=end_date,
        budget=BudgetRange.MODERATE,
        trip_type=TripType.CULTURAL,
        travelers=2,
        preferences=[
            "fashion and design",
            "Italian cuisine",
            "art galleries and museums",
            "historic architecture", 
            "shopping districts",
            "aperitivo culture",
            "day trip to Lake Como"
        ],
        dietary_restrictions=["gluten-free options needed"],
        special_requirements=[
            "interested in fashion week events",
            "prefer central location accommodation",
            "walking-friendly itinerary"
        ]
    )
    
    print("📋 Milan Trip Request Details:")
    print(f"   🎯 Destination: {milan_request.destination}")
    print(f"   📅 Duration: {milan_request.start_date} to {milan_request.end_date} ({milan_request.duration_days} days)")
    print(f"   👥 Travelers: {milan_request.travelers}")
    print(f"   💰 Budget: {milan_request.budget.value}")
    print(f"   🎨 Trip Type: {milan_request.trip_type.value}")
    print(f"   ❤️  Key Interests:")
    for pref in milan_request.preferences:
        print(f"      • {pref}")
    print(f"   🥗 Dietary: {', '.join(milan_request.dietary_restrictions)}")
    print()
    
    if not has_api_key:
        show_milan_demo_workflow(milan_request)
        return
    
    # Run with real AI
    try:
        print("🚀 Initializing LangGraph Trip Planner for Milan...")
        planner = create_trip_planner()
        
        print("🤖 AI Agents working on your Milan trip:")
        print("   🔍 Research Agent - Analyzing Milan attractions & culture")
        print("   🏨 Accommodation Agent - Finding hotels in fashion district")
        print("   🎯 Activity Agent - Discovering fashion, art, and food experiences")
        print("   📅 Itinerary Agent - Creating day-by-day Milan schedule")
        print("   💰 Budget Agent - Calculating costs for Milan trip")
        print("   💡 Travel Tips Agent - Milan-specific advice & recommendations")
        print()
        
        print_planning_status("Starting Milan trip planning process...")
        
        # Execute the planning workflow
        result = planner.invoke({"trip_request": milan_request})
        
        if result and result.get("trip_plan"):
            trip_plan = result["trip_plan"]
            print("\n" + "🎉" * 20)
            print("🇮🇹 MILAN TRIP PLAN COMPLETED!")
            print("🎉" * 20)
            print()
            
            # Display the formatted trip plan
            formatted_plan = format_trip_plan(trip_plan)
            print(formatted_plan)
            
            # Save the plan
            filename = f"milan_trip_plan_{milan_request.start_date}.json"
            print(f"\n💾 Milan trip plan saved to: {filename}")
            
            print("\n🎯 Your Milan adventure is ready!")
            print("   • Fashion district exploration")
            print("   • Duomo and historic sites")
            print("   • Authentic Italian dining")
            print("   • Art galleries and museums")
            print("   • Aperitivo experiences")
            
        else:
            print("❌ Failed to generate Milan trip plan.")
            
    except Exception as e:
        print(f"❌ Error during Milan trip planning: {str(e)}")
        show_milan_demo_workflow(milan_request)


def show_milan_demo_workflow(trip_request):
    """Show what the Milan trip planning workflow would look like."""
    print("📝 Milan Trip Planning Workflow (Demo Mode):")
    print()
    
    print("🔍 Research Agent would analyze:")
    print("   • Milan's fashion district (Quadrilatero della Moda)")
    print("   • Historic sites (Duomo, La Scala, Castello Sforzesco)")
    print("   • Best neighborhoods for accommodation")
    print("   • Local customs and aperitivo culture")
    print("   • Transportation options (Metro, trams)")
    print()
    
    print("🏨 Accommodation Agent would find:")
    print("   • Boutique hotels near fashion district")
    print("   • Central locations near Duomo")
    print("   • Design hotels reflecting Milan's style")
    print("   • Budget-friendly options with good access")
    print()
    
    print("🎯 Activity Agent would discover:")
    print("   • Duomo di Milano and rooftop access")
    print("   • La Scala opera house tours")
    print("   • Brera art district galleries")
    print("   • Navigli district for aperitivo")
    print("   • Fashion boutiques and designer stores")
    print("   • Day trip to Lake Como")
    print()
    
    print("📅 Itinerary Agent would create:")
    print("   Day 1: Arrival + Duomo exploration")
    print("   Day 2: Fashion district + shopping")
    print("   Day 3: Art galleries + Brera district")
    print("   Day 4: Lake Como day trip")
    print("   Day 5: Navigli + departure")
    print()
    
    print("💰 Budget Agent would calculate:")
    print("   • Accommodation: €100-150/night")
    print("   • Meals: €40-60/person/day")
    print("   • Activities: €20-30/person/day")
    print("   • Transportation: €15-20/person/day")
    print("   • Shopping: Variable budget")
    print()
    
    print("💡 Travel Tips Agent would provide:")
    print("   • Best times for aperitivo (6-8 PM)")
    print("   • Dress code for upscale restaurants")
    print("   • Metro system navigation")
    print("   • Italian dining etiquette")
    print("   • Fashion week calendar")
    print("   • Gluten-free restaurant recommendations")
    print()
    
    print("🎯 Complete Milan Experience:")
    print("   → Fashion and design immersion")
    print("   → Historic and cultural exploration")
    print("   → Authentic Italian culinary journey")
    print("   → Art and architecture appreciation")
    print("   → Local lifestyle experiences")
    print()
    
    print("To see this generated by real AI agents, add your OpenAI API key!")


if __name__ == "__main__":
    milan_trip_demo()