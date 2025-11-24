"""
Build a single AI agents with use of custom Tools implemented locally.

"""

from agentic_learning.tools import research_tools
from openai import OpenAI
import json
import os

#### TOOLS ####

# Tool mapping
TOOL_MAPPING = {
    "tavily_search_tool": research_tools.tavily_search_tool,
    "arxiv_search_tool": research_tools.arxiv_search_tool,
}

def generate_research_report_with_tools(prompt: str, model: str = "gpt-4o") -> str:
    """
    Generates a research report using OpenAI's tool-calling with arXiv and Tavily tools.

    Args:
        prompt (str): The user prompt.
        model (str): OpenAI model name.

    Returns:
        str: Final assistant research report text.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a research assistant that can search the web and arXiv to write detailed, "
                "accurate, and properly sourced research reports.\n\n"
                "🔍 Use tools when appropriate (e.g., to find scientific papers or web content).\n"
                "📚 Cite sources whenever relevant. Do NOT omit citations for brevity.\n"
                "🌐 When possible, include full URLs (arXiv links, web sources, etc.).\n"
                "✍️ Use an academic tone, organize output into clearly labeled sections, and include "
                "inline citations or footnotes as needed.\n"
                "🚫 Do not include placeholder text such as '(citation needed)' or '(citations omitted)'."
            )
        },
        {"role": "user", "content": prompt}
    ]

    # List of available tools
    tools = [research_tools.arxiv_tool_def, research_tools.tavily_tool_def]

    # Maximum number of turns
    max_turns = 3
    
    CLIENT = OpenAI()

    # Iterate for max_turns iterations
    for _ in range(max_turns):

        ### START CODE HERE ###

        # Chat with the LLM via the client and set the correct arguments. 
        # Make sure to let the LLM choose tools automatically.
        response = CLIENT.chat.completions.create( 
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=1, 
        ) 

        ### END CODE HERE ###

        # Get the response from the LLM and append to messages
        msg = response.choices[0].message 
        messages.append(msg) 

        # Stop when the assistant returns a final answer (no tool calls)
        if not msg.tool_calls:      
            final_text = msg.content
            print("✅ Final answer:")
            print(final_text)
            break

        # Execute tool calls and append results
        for call in msg.tool_calls:
            tool_name = call.function.name
            args = json.loads(call.function.arguments)
            print(f"🛠️ {tool_name}({args})")

            try:
                tool_func = TOOL_MAPPING[tool_name]
                result = tool_func(**args)
            except Exception as e:
                result = {"error": str(e)}

            ### START CODE HERE ###

            # Keep track of tool use in a new message
            new_msg = { 
                # Set role to "tool" (plain string) to signal a tool was used
                "role": "tool",
                # As stated in the markdown when inspecting the ChatCompletionMessage object 
                # every call has an attribute called id
                "tool_call_id": call.id,
                # The name of the tool was already defined above, use that variable
                "name": tool_name,
                # Pass the result of calling the tool to json.dumps
                "content": json.dumps(result)
            }

            ### END CODE HERE ###

            # Append to messages
            messages.append(new_msg)

    return final_text

def reflection_and_rewrite(report, model: str = "gpt-4o-mini", temperature: float = 0.3) -> dict:
    """
    Generates a structured reflection AND a revised research report.
    Accepts raw text OR the messages list returned by generate_research_report_with_tools.

    Returns:
        dict with keys:
          - "reflection": structured reflection text
          - "revised_report": improved version of the input report
    """

    # Input can be plain text or a list of messages, this function detects and parses accordingly
    report = research_tools.parse_input(report)

    ### START CODE HERE ###

    # Define the prompt. A multi-line f-string is typically used for this.
    # Remember it should ask the model to output ONLY valid JSON with this structure:
    # {{ "reflection": "<text>", "revised_report": "<text>" }}
    user_prompt = f"""
    
    You are a scientific writer assistant.
    
    Your task is to review a draft version of a reserach report, provide feedback and suggest a enhanced version.
    
    The feedback and revision should cover **exactly** the following items :
    - Srengths, 
    - limitations, 
    - suggestions, and 
    - opportunities.
    
    You must **STRICTLY** output the response with the following json schema:

    {{ "reflection": "<text>", "revised_report": "<text>" }}
    
    Input report:
    <input_report>{report}</input_report>
    
    Output only the JSON object and nothing else.
    """
    
    CLIENT = OpenAI()

    # Get a response from the LLM
    response = CLIENT.chat.completions.create( 
        # Pass in the model
        model=model,
        messages=[ 
            # System prompt is already defined
            {"role": "system", "content": "You are an academic reviewer and editor."},
            # Add user prompt
            {"role": "user", "content": user_prompt},
        ],
        # Set the temperature equal to the temperature parameter passed to the function
        temperature=temperature
    )

    ### END CODE HERE ###

    # Extract output
    llm_output = response.choices[0].message.content.strip()

    # Check if output is valid JSON
    try:
        data = json.loads(llm_output)
    except json.JSONDecodeError:
        raise Exception("The output of the LLM was not valid JSON. Adjust your prompt.")

    return {
        "reflection": str(data.get("reflection", "")).strip(),
        "revised_report": str(data.get("revised_report", "")).strip(),
    }

def convert_report_to_html(report, model: str = "gpt-4o", temperature: float = 0.5) -> str:
    """
    Converts a plaintext research report into a styled HTML page using OpenAI.
    Accepts raw text OR the messages list from the tool-calling step.
    """

    # Input can be plain text or a list of messages, this function detects and parses accordingly
    report = research_tools.parse_input(report)

    # System prompt is already provided
    system_prompt = "You convert plaintext reports into full clean HTML documents."

    ### START CODE HERE ###
    
    # Build the user prompt instructing the model to return ONLY valid HTML
    user_prompt = f"""
    Your task is to convert a plain text into HTML output.
    
    INPUT:
    <plain_text>{report}</plain_text>
    
    The output should be **strictly** with HTML format.
    
    Ensure the output is valid, clean HTML with appropriate section headers, formatted paragraphs, and clickable links.

    Preserve the citation style and request that the model responds only with HTML, without additional commentary.

    The output must only the final HTML result and nothing else.
    
    """
    
    CLIENT = OpenAI()

    # Call the LLM by interacting with the CLIENT. 
    # Remember to set the correct values for the model, messages (system and user prompts) and temperature
    response = CLIENT.chat.completions.create( 
        # Pass in the model
        model=model,
        messages=[ 
            # System prompt is already defined
            {"role": "system", "content": "You are a helpfull assistant"},
            # Add user prompt
            {"role": "user", "content": user_prompt},
        ],
        # Set the temperature equal to the temperature parameter passed to the function
        temperature=temperature
    )

    ### END CODE HERE ###

    # Extract the HTML from the assistant message
    html = response.choices[0].message.content.strip()  

    return html

#### MAIN ####

if __name__ == "__main__":

    prompt_ = "Multi AI Agents system evaluation"

    # 1) Initial Research Report 
    preliminary_report = generate_research_report_with_tools(prompt_)
    print("=== Research Report (preliminary) ===\n")
    print(preliminary_report)

    # 2) Reflection on the report (use the final TEXT to avoid ambiguity)
    reflection_text = reflection_and_rewrite(preliminary_report)   # <-- pass text, not messages
    print("=== Reflection on Report ===\n")
    print(reflection_text['reflection'], "\n")
    print("=== Revised Report ===\n")
    print(reflection_text['revised_report'], "\n")


    # 3) Convert the report to HTML (use the TEXT and correct function name)
    html = convert_report_to_html(reflection_text['revised_report'])

    print("=== Generated HTML (preview) ===\n")
    print((html or "")[:600], "\n... [truncated]\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(script_dir, "data", "output")
    os.makedirs(output_dir, exist_ok=True)

    # Get the script name
    script_name = os.path.basename(__file__).split(".")[0]

    # Dump the HTML into a file
    with open(f"{output_dir}/{script_name}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("=== Generated HTML (dumped to file) ===\n")
