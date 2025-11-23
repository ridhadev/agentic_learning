# Agentic Learning Library

This library is designed to facilitate the learning and implementation of agentic and multi-agentic coding patterns. It provides a structured, modular approach to building AI agents, managing their state, orchestrating multi-agent workflows, and evaluating their performance across various frameworks.

## Objective

The primary objective of this module is to serve as a comprehensive educational and experimental sandbox for:
- **Understanding Core Patterns**: Implementing fundamental agentic patterns like Reflection, ReAct, and Planning.
- **Multi-Agent Orchestration**: Exploring how multiple agents collaborate through routing, handoffs, and supervision.
- **Framework Agnosticism**: demonstrating how to build agents that can leverage different underlying LLM providers and frameworks (LangChain, AISuite).
- **Evaluation & Benchmarking**: Providing tools to rigorously measure agent performance using both deterministic metrics and LLM-as-a-judge approaches.

## Quick Start

### Prerequisites

- Python 3.10+
- Conda (Anaconda or Miniconda)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd agentic_learning
    ```

2.  **Set up the environment**:
    You can use the provided helper script to create a Conda environment named `agentic_learning` and install all dependencies:

    ```bash
    chmod +x setup_env.sh
    ./setup_env.sh
    ```

    **Or manually**:

    ```bash
    conda create -n agentic_learning python=3.10 -y
    conda activate agentic_learning
    pip install -r requirements.txt
    ```

3.  **Activate the environment**:
    ```bash
    conda activate agentic_learning
    ```

## Package Structure

The package is organized into logical modules, each serving a specific layer of the agentic stack:

```text
agentic_learning/
├── __init__.py
├── core/                               # Fundamental abstractions & Interfaces
│   ├── __init__.py
│   ├── agent.py                        # Base Agent class defining the standard protocol for all agents.
│   ├── memory.py                       # Classes for managing conversation history and state persistence.
│   ├── message.py                      # Standardized message data classes (System, User, Assistant).
│   └── tool.py                         # Base Tool class and decorators for defining agent capabilities.
├── patterns/                           # Implementation of specific Agentic Design Patterns
│   ├── __init__.py
│   ├── single_agent/                   # Patterns involving a single autonomous agent
│   │   ├── __init__.py
│   │   ├── reflection.py               # Implementation of the Reflection pattern (Self-Correction/Critique).
│   │   ├── react.py                    # Implementation of the ReAct (Reasoning + Acting) loop.
│   │   └── planning.py                 # Implementation of explicit step-by-step planning and execution.
│   └── multi_agent/                    # Patterns involving multiple collaborating agents
│       ├── __init__.py
│       ├── router.py                   # Logic for classifying user intent and routing to specialized agents.
│       ├── handoff.py                  # Mechanisms for transferring control and context between agents.
│       ├── supervisor.py               # A centralized orchestrator managing a team of sub-agents.
│       └── swarm.py                    # Decentralized, collaborative multi-agent systems without a central leader.
├── integrations/                       # Adapters for external libraries and model providers
│   ├── __init__.py
│   ├── providers/                      # Direct API wrappers for model providers (OpenAI, Anthropic, Mistral).
│   ├── langchain/                      # Specific implementations and adapters for the LangChain ecosystem.
│   └── aisuite/                        # Specific implementations and adapters for the AISuite framework.
├── tools/                              # Library of reusable tools for agents
│   ├── __init__.py
│   ├── web.py                          # Tools for web searching, scraping, and browser interaction.
│   ├── data.py                         # Tools for data analysis, SQL querying, and pandas manipulation.
│   └── system.py                       # Tools for file system operations and shell command execution.
├── evaluation/                         # Framework for testing and evaluating agents
│   ├── __init__.py
│   ├── judges.py                       # LLM-as-a-Judge implementations for qualitative assessment.
│   ├── metrics.py                      # Deterministic metrics for quantitative assessment (accuracy, latency).
│   └── tracing.py                      # Utilities for logging, tracing execution flows, and debugging.
└── utils/                              # Shared utility functions and configuration
    ├── __init__.py
    ├── config.py                       # Environment configuration and settings management.
    └── utils.py                        # General helper functions for API clients, image encoding, and display.
```
