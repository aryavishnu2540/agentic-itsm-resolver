🤖 Agentic ITSM Auto-Resolver

An autonomous IT Service Management (ITSM) agent built with Python. This project demonstrates how to transition from using LLMs as simple chatbots to building an Agentic Workflow capable of interacting with local backend systems and executing physical database updates.

📖 Overview

Enterprise IT support is often bottlenecked by repetitive L1/L2 tickets (e.g., password resets, database provisioning). This system acts as a digital sysadmin. It intercepts natural language IT requests, evaluates them against standard operating procedures, autonomously selects the appropriate backend Python tool, executes the fix, and logs a structured closure report.

🧠 Core AI Architecture Concepts Used

This project was built to specifically master the four pillars of the Anthropic Messages API:

Stateless State Management: The Python orchestrator handles the conversation history, routing alternating user/assistant roles to maintain multi-turn context without relying on UI-layer memory.

Native Tool Calling (Function Calling): The agent does not hallucinate actions. It is provided with strict JSON schemas of local Python functions. When it decides an action is needed, it triggers a tool_use stop reason, waits for the Python backend to execute the function, and ingests the tool_result.

Prompt Caching: To simulate enterprise-scale efficiency, the core IT Playbook (System Prompt) uses cache_control: ephemeral. In a production environment, this reduces latency and slashes API token costs by up to 90%.

Structured Outputs: The agent's final state is restricted to structured data generation. It outputs a strictly formatted JSON payload to act as an automated database audit log.

📂 Project Structure

itsm-auto-resolver/
├── database.json          # Persistent local data layer (Users & Tickets)
├── tools_blueprint.py     # Backend functions (DB read/write logic)
└── main.py                # Central AI orchestrator and terminal UI


⚙️ How the Loop Works

Input: User submits an IT support ticket via the terminal.

Evaluation: The orchestrator packages the ticket with the cached system playbook and tool schemas, sending it to the simulated LLM engine.

Execution: If a tool is required (e.g., reset_user_password), the agent triggers the local Python function in tools_blueprint.py, dynamically altering database.json.

Resolution: The agent returns a strict JSON payload detailing the resolution status, acting as a permanent system log.

Note on Development: This repository currently utilizes a MockAnthropicClient for local development and testing. This architectural choice allows for rapid iteration of the agentic tool loop and JSON parsing logic without consuming live API budget. It can be instantly swapped to the live anthropic SDK for production.

🚀 Getting Started

1. Clone the repository:

git clone [https://github.com/YourUsername/agentic-itsm-resolver.git](https://github.com/YourUsername/agentic-itsm-resolver.git)
cd agentic-itsm-resolver


2. Install dependencies:

pip install anthropic


3. Run the interactive agent:

python main.py
