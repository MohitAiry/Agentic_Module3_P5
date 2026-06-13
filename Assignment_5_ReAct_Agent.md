# Assignment 5: Building a ReAct Agent from Scratch

## Course Module
**Agentic AI Systems – Agent Execution Patterns**

### Learning Objectives
By the end of this assignment, you will be able to:
1. Implement the Observe → Think → Act → Evaluate loop from scratch.
2. Understand the core execution engine of frameworks like LangChain, CrewAI, and AutoGen.
3. Handle multi-tool workflows where one tool's output feeds directly into the next decision.
4. Experience the ReAct (Reason + Act) pattern to create traceable, debuggable reasoning chains.

---

## Background: What is a ReAct Agent?
Modern Large Language Models (LLMs) often cannot solve complex problems in a single pass. Instead, they follow a cyclic execution pattern known as the **ReAct (Reason + Act) Framework**.

The agent alternates between:
- **Thinking** about what it needs to do next.
- Choosing an **Action** (calling a tool).
- **Observing** the result of that action.
- Updating its context to continue reasoning until a final answer is achieved.

### Real World Example
If a user asks: *"What is India's GDP in USD converted to INR?"*
A static LLM prompt might fail or hallucinate. A ReAct Agent, however, dynamically resolves this:

```
Thought: I need India's GDP.
Action: web_search("India GDP")
Observation: 3.94 trillion USD

Thought: Now I need the exchange rate for USD to INR.
Action: get_exchange_rate("INR")
Observation: 83.0

Thought: I will use the calculator to multiply these values.
Action: calculator("3.94e12 * 83")
Observation: 327020000000000

Answer: India's GDP is approximately 327 trillion INR.
```

---

## Problem Statement
Your task is to **build a ReAct-style AI agent from scratch** in Python, without using any external agent frameworks. The agent must loop through multi-step reasoning to answer research and calculation questions.

### Available Tools to Implement
You must implement the following 3 mock tools in your script:

1. **`web_search(query: str)`** 
   - *Purpose*: Retrieve information from a local JSON dictionary.
   - *Mock Data*: `{"india gdp": "3.94 trillion USD", "usa gdp": "29.16 trillion USD"}`

2. **`calculator(expression: str)`**
   - *Purpose*: Evaluate a Python arithmetic expression safely.
   - *Hint*: Use `eval(expression, {"__builtins__": None}, {})`.

3. **`get_exchange_rate(currency: str)`**
   - *Purpose*: Return a hardcoded exchange rate dict (e.g., `{"INR": 83.0}`).

4. **Optional**: **`date_difference(date1: str, date2: str)`**
   - *Purpose*: Calculate days between two dates.

### Questions the Agent Must Answer
1. “What is the GDP of India in USD, converted to INR?”
2. “If a product costs $150 and there is a 18% GST, what is the final price in INR?”
3. “How many days are there between January 15, 2025 and August 20, 2026?”

### Requirements
1. **Trace Logs**: The agent must print each `Thought` → `Action` → `Observation` step explicitly to the console.
2. **Iteration Limit**: Set a maximum of 8 iterations per question. If the agent fails to resolve it within 8 steps, it must print: *"Could not resolve within iteration limit."*
3. **Termination**: The loop must safely terminate when the LLM outputs a final `Answer:` token.

---

## Getting Started

### Suggested Project Structure
```text
project/
│
├── main.py             # Main script containing your LLM loop
├── llm.py              # LLM integration (e.g. calling Ollama)
├── tools.py            # Tool implementations (web_search, calculator, etc.)
├── search_data.json    # Local JSON file for mock web searches
└── outputs.txt         # Saved traces
```

### Under the Hood: How ReAct Actually Works
A ReAct agent is essentially a `while` or `for` loop wrapped around an LLM call and some string parsing. Here is exactly how the magic happens in code:

#### 1. The System Prompt constraint
The core of the framework is a strict system prompt. You must force the LLM to output its response in an exact format so your Python code can parse it reliably using Regular Expressions (`regex`).

```python
SYSTEM_PROMPT = """You are a reasoning agent.
You must solve the question by following this exact format:
Thought: <your reasoning here>
Action: tool_name("arguments")

Wait for the 'Observation:' from the system. Do NOT generate it yourself.
Once you have enough info, output:
Answer: <final answer>
"""
```

#### 2. The Context Loop
The agent maintains a running "memory" of the conversation in a variable, often called `context`. In each iteration, it sends the *entire* history back to the LLM.

```python
context = f"{SYSTEM_PROMPT}\n\nQuestion: {question}\n"

for iteration in range(MAX_ITERATIONS):
    # Pass the entire accumulated history to the model
    response = call_llm(context).strip()
    
    # Immediately append the model's new thought/action to our history
    context += response + "\n"
```

#### 3. String Parsing (Regex)
The LLM outputs pure text. The ReAct framework's job is to parse that text to figure out what tool the LLM wants to run. We use Python's `re` module for this.

```python
    import re
    # We look for the literal string "Action:" followed by a function name and arguments
    action_match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
    
    if action_match:
        tool_name = action_match.group(1) # e.g., 'web_search'
        args_str = action_match.group(2)  # e.g., '"India GDP"'
```

#### 4. Dynamic Tool Execution & Observation
Once we know what tool the LLM wants, we map the string name (e.g., `"web_search"`) to an actual Python function.

```python
        # Safely parse the arguments string into actual Python variables
        args = parse_args(args_str) 
        
        # Execute the matched tool dynamically
        if tool_name in TOOLS:
            observation = TOOLS[tool_name](*args)
        
        # Give the result BACK to the LLM by appending it to the context
        context += f"Observation: {observation}\n"
```
By appending the `Observation` to the `context`, the next time the `for` loop runs, the LLM will "see" the result of its action and can generate its next `Thought`.

### Deliverables
1. **`main.py`, `llm.py`, `tools.py`**: Your complete, standalone and modular ReAct loop implementation.
2. **`outputs.txt`**: A text file containing the full thought/action/observation traces for all 3 questions.

---

## Evaluation Rubric (100 Marks)
| Component | Marks |
| :--- | :--- |
| Tool Implementation (Python definitions) | 20 |
| ReAct Loop Logic & Condition Handling | 25 |
| Parsing & Tool Orchestration | 15 |
| Multi-Step Tool Chaining execution | 15 |
| Clean Thought-Action-Observation Trace | 15 |
| Code Quality & Safety (e.g. safe `eval`) | 10 |

---
**Professor's Note**: The goal of this assignment is NOT just to get the answers to the 3 questions. It is to build the fundamental "execution engine". Once you deeply understand this `Observe -> Think -> Act` loop, popular tools like LangChain or AutoGen will simply look like helpful abstractions built on top of the system you just wrote. Good luck!
