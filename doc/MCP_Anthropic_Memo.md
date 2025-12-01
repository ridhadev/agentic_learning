# MCP Anthropic Memo

## Introduction
This is a memo of the MCP Anthropic course from Deeplearning.AI taken in 2025.
[Course Link](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/)

## Defintion 

1. MCP = a standard protocol for LLM–tool/data connectivity
    • Definition: The Model Context Protocol (MCP) is an open protocol that standardizes how LLM applications connect to and work with tools and external data sources.

2. MCP is inspired by existing successful standards
    • It plays a similar role to REST APIs (standardizing how web apps interact with backends) and LSP (standardizing how IDEs interact with language tools).
    • MCP follows the same philosophy: build once, use everywhere.

    ![what_is_mcp](./images/mcp/what_is_mcp.png)

3. Everything MCP does can be done without MCP — but MCP makes it scalable
    • You can manually write integrations between your model and each data source.
    • But MCP saves massive duplicated effort by providing a shared, consistent, reusable interface across all models and applications.
    ![std_ai_dev](./images/mcp/std_ai_dev.png)

4. MCP enables seamless natural-language interaction with external systems
    • With a few lines of code, an app can read/write from systems like GitHub, Asana, Google Drive, CRM tools, databases, etc.
    • Developers can build or reuse community MCP servers to integrate with any system.
    
 ![how_it_works](./images/mcp/how_does_it_work.png)

## MCP Architecture
 ![mcp_architecture](./images/mcp/mcp_archi.png)

![mcp_tool](./images/mcp/mcp_tool.png)
![mcp_resource](./images/mcp/mcp_resource.png)
![mcp_templates](./images/mcp/templates.png)
![mcp_prompts](./images/mcp/prompts.png)

![mcp_transport](./images/mcp/mcp_transport.png)
![http_transport](./images/mcp/http_transport.png)
![streamable_http_transport](./images/mcp/streamable_http.png)























