#!/usr/bin/env python3
"""
Simple test script for F1 Agent functionality
"""

from f1_agent import create_f1_agent, MessageType

def test_basic_functionality():
    """Test basic agent functionality"""
    print("=" * 50)
    print("Testing F1 Agent Basic Functionality")
    print("=" * 50)
    
    # Create agent
    print("Creating agent...")
    agent = create_f1_agent("Lewis Hamilton", "ferrari")
    print(f"✅ Agent created: {agent.context.driver_name} ({agent.context.team})")
    
    # Test Speak capability
    print("\n🎤 Testing Speak capability:")
    message = agent.speak()
    print(f"Generated message: '{message}'")
    
    # Test Act capability - Post status
    print("\n📱 Testing Act capability - Post Status:")
    action = agent.act_post_status("Testing the agent functionality!")
    print(f"Posted: '{action.content}'")
    print(f"Engagement: {action.metadata.get('engagement')} interactions")
    
    # Test Act capability - Reply to comment
    print("\n💬 Testing Act capability - Reply to comment:")
    reply_action = agent.act_reply_to_comment("Great drive today, Lewis!")
    print(f"Fan comment: 'Great drive today, Lewis!'")
    print(f"Reply: '{reply_action.content}'")
    print(f"Sentiment detected: {reply_action.metadata.get('original_sentiment')}")
    
    # Test Think capability - Show context
    print("\n🧠 Testing Think capability - Show context:")
    context = agent.think_show_context()
    print(f"Driver: {context['driver_info']['name']}")
    print(f"Team: {context['driver_info']['team']}")
    print(f"Circuit: {context['current_situation']['circuit']}")
    print(f"Mood: {context['current_situation']['mood']}")
    
    # Test Think capability - Update context
    print("\n🔄 Testing Think capability - Update context:")
    success = agent.think_update_context(
        current_circuit="monaco",
        mood="ecstatic"
    )
    if success:
        print("✅ Context updated successfully")
        updated_context = agent.think_show_context()
        print(f"New circuit: {updated_context['current_situation']['circuit']}")
        print(f"New mood: {updated_context['current_situation']['mood']}")
    else:
        print("❌ Context update failed")
    
    # Test Race Weekend Simulation
    print("\n🏁 Testing Race Weekend Simulation:")
    print("Running shortened simulation...")
    simulation_results = agent.run_race_weekend_simulation("silverstone", "standard_weekend")
    
    print(f"Circuit: {simulation_results['circuit']}")
    print(f"Weekend type: {simulation_results['weekend_type']}")
    print(f"Sessions completed: {len(simulation_results['sessions'])}")
    
    # Show final race result
    final_session = simulation_results['sessions'][-1]
    print(f"Final race position: P{final_session['result']['position']}")
    print(f"Final race message: '{final_session['message']}'")
    print(f"Weekend summary: {simulation_results['final_status']}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed successfully!")
    print("F1 Agent is working correctly.")
    print("=" * 50)

if __name__ == "__main__":
    test_basic_functionality()