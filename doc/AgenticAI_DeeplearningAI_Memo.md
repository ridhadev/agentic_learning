# AgenticAI DeeplearningAI Memo

This is a memo of the AgenticAI course from Deeplearning.AI taken in 2025.
[Course Link](https://www.deeplearning.ai/short-courses/agentic-ai-apps-with-google-genai/)

## Reflection Pattern
    * Reflection is when agent review an ealier version of an output and enhance it
    
    * Reasoning is also called Thinking Models

![reflection_tools](./images/agentic_ai/reflection_tools.png)

    * Improvment may not be impressive but get better, compared to wero prompying for exampble) espcially when LLm has access to external information (ex: code, Run outout and then review the code)
    reflect

![reflection_perf](./images/agentic_ai/reflection_perf.png)

## Tools
    • Tools are functions that LLM may make use of.
    
    • Usullay we say LLMs call the function/tool but actually the LLM identify the tool it may use at each step and make a request to use it (set in its JSON response under response.choices[0].message.tool_calls)

    • The call may be automatic or manual (wait for LLM response, if a tool is requested retrieve that tool and arguments and excute it, then pass the tool results and the history of message to the LLM again to continue the execution and formulate a last response or identify another tool)=> Developer provides function, LLM decides to use it, LLM outputs request, developer’s system executes the function, result fed back to LLM
    
![tool_calls](./images/agentic_ai/simple_tool.png)
![behind_the_scene](./images/agentic_ai/behind_scene.png)
![behind_the_scene_calls](./images/agentic_ai/behind_scene_2.png)


    • Using aisuits open lib of this course , if the set of tools is provided as function the excution is automatic, The parameter max_turns define the maximum number of steps or iteration whan LLM can request a tool call
    
    • If the set of tool is provided as sequence of json objects than aisuite presume tha call will be manual and n oneed to specify max_turns
    - Both manual and auto calls are handled in the first lab of the chapter.

## Evaluation

Evaluation strategy

- Test and evaluate each output of the agent seperatly

- Start by identifying the weak points of the chain, so we can start work on it and priorittize it.

![step_by_step_eval](./images/agentic_ai/step_by_step_eval.png)

- Two by two evaluation type : 
    - Objective (code based) Versus Subjective (Judgement based)
    - Ground truth Versus No Ground truth

![Evlauation_grid](./images/agentic_ai/Evaluations-Objective-Subjective-Matrix.png)

The code in ./evaluation/web_search_eval.py implement a task based with ground truth evaluation.

## Patterns for Highly Autonomous Agents

### PLANNING Pattern

    • PLANNING pattern : widely used patterns where AI plan a sequence of steps to execute, providing a PROMPT and serie of TOOLS

    • The sequence is NOT predefined (challenging for dev)


Instead of high level description some developer ask to output the plan in JSON (or XML) code to better follow the plan and expose it to downstream code in order to execute in more reliable way (rather than plain text)
plan_json

![plan_json](./images/agentic_ai/plan_json.png)

#### Plan with Code Execution
- Ask LLM to plan execution through Code instead of JSON format
- This is usefull when number of queries or complex query cannot be covered by tools and requires a huge number of tools.
- The LLM generate Code with multiple steps (eaxh comment is a step)

![plan_code](./images/agentic_ai/plan_code.png)

### Multi-agents collaboration

####  Sequantial pattern with predefined steps

![seq_pattern](./images/agentic_ai/seq_pattern.png)


#### Manager allocating task to a team of agents

This Hierarchical pattern (each team members communicate or go through the manager)

![com_pattern](./images/agentic_ai/com_pattern.png)

Can go further with Deep Hierarchical design pattern where each team agent has some sub-team agents

![deep_pattern](./images/agentic_ai/deep_pattern.png)

Or All-to-ALL (more chaos and unpredictibility) each agent communicate with another and once receive a message respond to that sender or excute it

![all_to_all](./images/agentic_ai/all_to_all_pattern.png)

