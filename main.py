import json
from tools_blueprint import reset_user_password, provision_cloud_db

# ==========================================
# 1. THE MOCK API CLIENT (Cost: $0.00)
# ==========================================
class MockAnthropicClient:
    class Messages:
        # FIX: We changed 'tools' to 'tools=None' to make it optional!
        def create(self, model, max_tokens, system, messages, tools=None):
            print("\n[☁️ MOCK API]: Request intercepted! Simulating Claude's brain locally...")
            
            # If this is the first prompt, simulate Claude deciding to use the password tool
            if len(messages) == 1:
                class ToolBlock:
                    type = "tool_use"
                    name = "reset_user_password"
                    id = "mock_tool_001"
                    input = {"employee_id": "EMP-849"}
                    
                class MockResponse:
                    stop_reason = "tool_use"
                    content = [ToolBlock()]
                return MockResponse()
                
            # If this is the second prompt (after the tool runs), simulate the final JSON output
            else:
                class TextBlock:
                    text = '{\n  "ticket_status": "CLOSED",\n  "action_taken": "Account Unlocked via Python Tool",\n  "employee_notified": true\n}'
                
                class MockResponse:
                    stop_reason = "end_turn"
                    content = [TextBlock()]
                return MockResponse()
                
    def __init__(self):
        self.messages = self.Messages()
                
    def __init__(self):
        self.messages = self.Messages()

# Initialize our free local mock client instead of the real one
client = MockAnthropicClient()


# ==========================================
# 2. THE REAL ARCHITECTURE LOOP
# ==========================================
tools_schema = [
    {
        "name": "reset_user_password",
        "description": "Unlocks a corporate account and resets the password.",
        "input_schema": {
            "type": "object",
            "properties": {"employee_id": {"type": "string"}},
            "required": ["employee_id"]
        }
    }
]

system_playbook = [{"type": "text", "text": "You are an automated IT Agent.", "cache_control": {"type": "ephemeral"}}]

def run_auto_resolver(ticket_text):
    messages = [{"role": "user", "content": ticket_text}]
    
    # The script calls our Mock Client, thinking it is the real Anthropic API
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        system=system_playbook,
        tools=tools_schema,
        messages=messages
    )
    
    if response.stop_reason == "tool_use":
        tool_call = [block for block in response.content if block.type == "tool_use"][0]
        tool_name = tool_call.name
        tool_inputs = tool_call.input
        
        print(f"[🤖 AGENT]: Decided to execute tool: {tool_name}")
        
        if tool_name == "reset_user_password":
            result = reset_user_password(tool_inputs["employee_id"])
            
        print(f"[⚙️ SYSTEM RESULT]: {result}")
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": tool_call.id, "content": result}]
        })
        
        final_response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=500,
            system="Output strict JSON.",
            messages=messages
        )
        print(f"\n[📊 DB PAYLOAD GENERATED]:\n{final_response.content[0].text}")

if __name__ == "__main__":
    print("="*60)
    print("🤖 Agentic ITSM Resolver Initialized.")
    print("Type 'exit' to shut down the server.")
    print("="*60)
    
    while True:
        # Prompt the user to type a ticket
        user_input = input("\n[👷 EMPLOYEE] Enter IT Support Ticket: ")
        
        # Check if the user wants to quit
        if user_input.lower() in ['exit', 'quit']:
            print("[🛑 SYSTEM] Shutting down agent...")
            break
            
        # Ignore empty entries
        if not user_input.strip():
            continue
            
        print("-" * 40)
        # Send the user's typed input to the orchestrator
        run_auto_resolver(user_input)
        print("-" * 40)