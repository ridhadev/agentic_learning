# Google AI Agents - 5 Days Course Summary

This document summarizes the key concepts, techniques, and definitions covered in the Google 5-Day Agentic AI course notebooks. It serves as a quick reference guide to the Google Agent Development Kit (ADK) and agentic patterns.

All notebooks are available in the `notebooks/google_5_days` directory.

## Day 1: Foundations & Architectures

### 1a: From Prompt to Action
**Goal:** Build a basic AI agent using ADK.
- **Core Components:**
  - **`Agent`**: The fundamental building block. Configured with a model (e.g., `Gemini`) and instructions.
  - **`InMemoryRunner`**: Orchestrates the agent's execution loop (User -> Agent -> Tools -> Agent -> User).
  - **Tools**: Capabilities given to the agent (e.g., `google_search`).
- **Key Concepts:**
  - **Prompt Engineering**: Defining the agent's persona and constraints via `instruction`.
  - **Tool Use**: How agents select and execute tools to fulfill requests.

### 1b: Agent Architectures
**Goal:** Compose multiple agents into complex systems.
- **Patterns:**
  - **Sequential**: Agents run one after another in a fixed pipeline. Output of Agent A -> Input of Agent B.
  - **Parallel**: Agents run concurrently on independent sub-tasks. Results are aggregated.
  - **Loop**: Agents iterate on a task until a condition is met (e.g., refinement).
  - **Manager/Router**: An LLM acts as a "manager" to delegate tasks to specialized sub-agents.
- **Key Components:**
  - **`SequentialAgent`, `ParallelAgent`, `LoopAgent`**: ADK classes for structural patterns.
  - **`AgentTool`**: Wraps an `Agent` as a tool, allowing other agents to call it.
  - **`output_key`**: Mechanism to pass specific state/data between agents in a flow.

## Day 2: Tools & Best Practices

### 2a: Agent Tools
**Goal:** Extend agent capabilities with custom and built-in tools.
- **Types of Tools:**
  - **Function Tools**: Python functions converted to tools. Requires type hints and docstrings.
  - **Agent Tools**: Using other agents as tools (hierarchical).
  - **Built-in Tools**: Pre-made tools like `google_search` or `BuiltInCodeExecutor` (for reliable math/logic).
- **Techniques:**
  - **`FunctionTool.from_function`**: Utility to convert Python functions.
  - **Docstrings**: Critical for the LLM to understand *when* and *how* to use the tool.

### 2b: Best Practices (MCP & LROs)
**Goal:** Advanced tool patterns and human-in-the-loop.
- **Model Context Protocol (MCP)**:
  - Standard for connecting AI assistants to systems (data, tools, prompts).
  - **`McpToolset`**: ADK wrapper to consume MCP servers (e.g., connecting to a local database or API via MCP).
- **Long-Running Operations (LROs)**:
  - Handling tasks that take time or require human approval.
  - **`ToolContext`**: Accessing runtime state within a tool.
  - **`ResumabilityConfig`**: Configuring an `App` to pause execution (e.g., for `adk_request_confirmation`) and resume later using an `invocation_id`.

## Day 3: Memory & Sessions

### 3a: Agent Sessions (Short-Term Memory)
**Goal:** Manage conversation history and state within a single interaction.
- **Concepts:**
  - **Session**: A container for a continuous conversation thread.
  - **Events**: Individual interactions (User message, Model response, Tool call).
  - **State**: Key-value storage for the session (`session.state`).
- **Components:**
  - **`SessionService`**: Manages storage.
    - `InMemorySessionService`: Volatile, for testing.
    - `DatabaseSessionService`: Persistent (e.g., SQLite), survives restarts.
  - **Context Compaction**: Automatically summarizing old conversation turns to save tokens. Configured via `EventsCompactionConfig` in an `App`.

### 3b: Agent Memory (Long-Term Memory)
**Goal:** Persist knowledge across different sessions.
- **Concepts:**
  - **Session vs. Memory**: Session is for *now* (context); Memory is for *later* (recall).
  - **Consolidation**: Extracting facts from raw conversation logs into structured memories (handled by managed services like Vertex AI Memory Bank).
- **Workflow:**
  1.  **Initialize**: `MemoryService` (e.g., `InMemoryMemoryService` or `VertexAiMemoryBankService`).
  2.  **Ingest**: `memory_service.add_session_to_memory(session)`.
  3.  **Retrieve**: Agents use tools to access memory.
- **Retrieval Tools:**
  - **`load_memory` (Reactive)**: Agent decides when to search memory. Efficient.
  - **`preload_memory` (Proactive)**: Automatically searches and injects relevant memories into context before every turn.

## Day 4: Observability & Evaluation

### 4a: Observability
**Goal:** Understand agent behavior, debug failures, and monitor performance.
- **Pillars**: Logs (events), Traces (flow/timing), Metrics (stats).
- **Tools:**
  - **`adk web`**: Local web UI for interactive debugging, viewing traces, and inspecting tool calls.
  - **`LoggingPlugin`**: Built-in plugin to capture standard logs.
  - **Custom Plugins**: Create classes inheriting from `BasePlugin` with hooks like `before_agent_callback`, `after_tool_callback`, etc.

### 4b: Evaluation
**Goal:** Proactively measure agent quality and detect regressions.
- **Concepts:**
  - **Evaluation Set (`.evalset.json`)**: Collection of test cases (input prompt + expected output/behavior).
  - **Metrics**:
    - **Response Match Score**: Text similarity between actual and expected response.
    - **Tool Trajectory Score**: Correctness of tool selection and parameters.
- **Workflow:**
  1.  Define `test_config.json` (thresholds).
  2.  Create test cases (can be saved from `adk web` sessions).
  3.  Run `adk eval` CLI.
- **User Simulation**: Using an LLM to simulate a user interacting with the agent to test dynamic flows.

## Day 5: Advanced & Deployment

### 5a: Agent2Agent (A2A) Communication
**Goal:** Enable agents to collaborate across networks, languages, and organizations.
- **Protocol**: Standardized HTTP/JSON protocol for agent interoperability.
- **Components:**
  - **`to_a2a()`**: Exposes an ADK agent as an A2A server. Auto-generates an **Agent Card** (metadata/contract).
  - **`RemoteA2aAgent`**: A client proxy that lets a local agent consume a remote A2A agent as if it were a local sub-agent.
- **Use Cases**: Microservices, third-party vendor integration, cross-team collaboration.

### 5b: Deployment
**Goal:** Move agents from notebook to production.
- **Platform**: **Vertex AI Agent Engine** (Managed, auto-scaling).
- **Configuration**:
  - `requirements.txt`: Dependencies.
  - `.agent_engine_config.json`: Resources (CPU, Memory, Instances).
- **Process**:
  1.  Structure code (agent.py, requirements.txt).
  2.  `adk deploy agent_engine ...`.
  3.  Interact via Vertex AI SDK (`agent_engines.get`, `stream_query`).
- **Memory Bank**: Production deployment supports enabling long-term memory persistence automatically.
