from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from datetime import datetime

from .models import AgentState, TripPlan
from .agents import (
    ResearchAgent, AccommodationAgent, ActivityAgent, 
    ItineraryAgent, BudgetAgent, TravelTipsAgent
)


class TripPlannerGraph:
    """LangGraph-based trip planner that orchestrates multiple specialized agents."""
    
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        self.research_agent = ResearchAgent(model_name)
        self.accommodation_agent = AccommodationAgent(model_name)
        self.activity_agent = ActivityAgent(model_name)
        self.itinerary_agent = ItineraryAgent(model_name)
        self.budget_agent = BudgetAgent(model_name)
        self.travel_tips_agent = TravelTipsAgent(model_name)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        # Define the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("research", self._research_step)
        workflow.add_node("find_accommodations", self._accommodation_step)
        workflow.add_node("find_activities", self._activity_step)
        workflow.add_node("create_itinerary", self._itinerary_step)
        workflow.add_node("calculate_budget", self._budget_step)
        workflow.add_node("generate_tips", self._tips_step)
        workflow.add_node("finalize_plan", self._finalize_step)
        
        # Define the flow
        workflow.set_entry_point("research")
        
        # Sequential flow with conditional branching
        workflow.add_edge("research", "find_accommodations")
        workflow.add_edge("find_accommodations", "find_activities")
        workflow.add_edge("find_activities", "create_itinerary")
        workflow.add_edge("create_itinerary", "calculate_budget")
        workflow.add_edge("calculate_budget", "generate_tips")
        workflow.add_edge("generate_tips", "finalize_plan")
        workflow.add_edge("finalize_plan", END)
        
        return workflow.compile()
    
    def _research_step(self, state: AgentState) -> Dict[str, Any]:
        """Research the destination."""
        print("🔍 Researching destination...")
        try:
            research_data = self.research_agent.research_destination(state)
            state.destination_research = research_data
            state.current_step = "research_complete"
            print(f"✅ Research complete for {state.trip_request.destination}")
        except Exception as e:
            error_msg = f"Research failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"destination_research": state.destination_research, 
                "current_step": state.current_step,
                "errors": state.errors}
    
    def _accommodation_step(self, state: AgentState) -> Dict[str, Any]:
        """Find accommodations."""
        print("🏨 Finding accommodations...")
        try:
            accommodations = self.accommodation_agent.find_accommodations(state)
            state.accommodations = accommodations
            state.current_step = "accommodations_complete"
            print(f"✅ Found {len(accommodations)} accommodation options")
        except Exception as e:
            error_msg = f"Accommodation search failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"accommodations": state.accommodations,
                "current_step": state.current_step,
                "errors": state.errors}
    
    def _activity_step(self, state: AgentState) -> Dict[str, Any]:
        """Find activities."""
        print("🎯 Finding activities...")
        try:
            activities = self.activity_agent.find_activities(state)
            state.activities = activities
            state.current_step = "activities_complete"
            print(f"✅ Found {len(activities)} activities")
        except Exception as e:
            error_msg = f"Activity search failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"activities": state.activities,
                "current_step": state.current_step,
                "errors": state.errors}
    
    def _itinerary_step(self, state: AgentState) -> Dict[str, Any]:
        """Create the itinerary."""
        print("📅 Creating itinerary...")
        try:
            itinerary = self.itinerary_agent.create_itinerary(state)
            state.itinerary = itinerary
            state.current_step = "itinerary_complete"
            print(f"✅ Created {len(itinerary)} day itinerary")
        except Exception as e:
            error_msg = f"Itinerary creation failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"itinerary": state.itinerary,
                "current_step": state.current_step,
                "errors": state.errors}
    
    def _budget_step(self, state: AgentState) -> Dict[str, Any]:
        """Calculate budget."""
        print("💰 Calculating budget...")
        try:
            budget_breakdown = self.budget_agent.calculate_budget(state)
            state.budget_breakdown = budget_breakdown
            state.current_step = "budget_complete"
            print("✅ Budget calculation complete")
        except Exception as e:
            error_msg = f"Budget calculation failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"budget_breakdown": state.budget_breakdown,
                "current_step": state.current_step,
                "errors": state.errors}
    
    def _tips_step(self, state: AgentState) -> Dict[str, Any]:
        """Generate travel tips."""
        print("💡 Generating travel tips...")
        try:
            tips_data = self.travel_tips_agent.generate_tips(state)
            # Store tips data for final plan
            state.travel_tips_data = tips_data
            state.current_step = "tips_complete"
            print("✅ Travel tips generated")
        except Exception as e:
            error_msg = f"Travel tips generation failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"current_step": state.current_step,
                "errors": state.errors}
    
    def _finalize_step(self, state: AgentState) -> Dict[str, Any]:
        """Finalize the trip plan."""
        print("📋 Finalizing trip plan...")
        try:
            # Extract tips data
            tips_data = getattr(state, 'travel_tips_data', {})
            
            # Create the final trip plan
            duration = (state.trip_request.end_date - state.trip_request.start_date).days + 1
            
            final_plan = TripPlan(
                destination=state.trip_request.destination,
                start_date=state.trip_request.start_date,
                end_date=state.trip_request.end_date,
                duration_days=duration,
                accommodations=state.accommodations,
                daily_itinerary=state.itinerary,
                budget_breakdown=state.budget_breakdown or {},
                travel_tips=tips_data.get("travel_tips", []),
                emergency_contacts=tips_data.get("emergency_contacts", []),
                packing_suggestions=tips_data.get("packing_suggestions", [])
            )
            
            state.final_plan = final_plan
            state.current_step = "complete"
            print("✅ Trip plan finalized!")
            
        except Exception as e:
            error_msg = f"Plan finalization failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"❌ {error_msg}")
        
        return {"final_plan": state.final_plan,
                "current_step": state.current_step,
                "errors": state.errors}
    
    def plan_trip(self, trip_request) -> AgentState:
        """Execute the complete trip planning workflow."""
        print(f"🚀 Starting trip planning for {trip_request.destination}")
        print(f"📅 {trip_request.start_date} to {trip_request.end_date}")
        print(f"👥 {trip_request.travelers} travelers, {trip_request.budget.value} budget")
        print(f"🎯 Trip type: {trip_request.trip_type.value}")
        print("-" * 50)
        
        # Initialize state
        initial_state = AgentState(trip_request=trip_request)
        
        # Execute the graph
        try:
            final_state = self.graph.invoke(initial_state)
            
            if final_state.errors:
                print("\n⚠️ Some errors occurred during planning:")
                for error in final_state.errors:
                    print(f"  - {error}")
            
            print("\n🎉 Trip planning complete!")
            return final_state
            
        except Exception as e:
            print(f"\n💥 Trip planning failed: {str(e)}")
            initial_state.errors.append(f"Graph execution failed: {str(e)}")
            return initial_state


def create_trip_planner(model_name: str = "gpt-4-turbo-preview") -> TripPlannerGraph:
    """Create a new trip planner instance."""
    return TripPlannerGraph(model_name)