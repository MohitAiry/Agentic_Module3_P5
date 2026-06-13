import re
import ast
from tools import TOOLS
from llm import call_llm

SYSTEM_PROMPT = """You are an advanced reasoning agent designed to solve problems using a multi-step ReAct (Reason + Act) loop.

You have access to the following tools:
1. web_search(query: str) - Retrieves facts from a search engine.
2. calculator(expression: str) - Evaluates a mathematical expression (e.g. 150 * 1.18).
3. get_exchange_rate(currency: str) - Returns the exchange rate for a given currency relative to USD (e.g. INR).
4. date_difference(date1: str, date2: str) - Returns the number of days between two dates formatted as "Month DD, YYYY".

To solve a question, you must follow this exact format:
Thought: Think about what you need to do next to solve the question.
Action: call exactly one tool using Python syntax, e.g., web_search("India GDP") or calculator("3.94e12 * 83") or get_exchange_rate("INR").

Wait for the "Observation:" from the system. Do NOT generate the "Observation:" yourself.
If you have all the information needed to answer the question, output:
Answer: The final answer to the user's question.

Always follow the exact format of Thought, Action, and Answer. Only use tools when you need information. Do not fabricate observations.
"""

def parse_args(args_str: str):
    """Safely parse tool arguments from a string."""
    try:
        if not args_str.strip():
            return ()
        return ast.literal_eval(f"({args_str},)" if "," not in args_str else f"({args_str})")
    except Exception:
        # Fallback to simple split
        return [arg.strip(" '\"") for arg in args_str.split(',')]

def run_agent(question: str, max_iterations: int = 8):
    print(f"\n Target Question: {question}\n")
    context = f"{SYSTEM_PROMPT}\n\nQuestion: {question}\n"
    
    for iteration in range(1, max_iterations + 1):
        print(f"--- [ Iteration {iteration} ] ---")
        
        # 1. REASON (LLM thinks about what to do next and decides on an action)
        response = call_llm(context).strip()
        
        if "Observation:" in response:
            response = response.split("Observation:")[0].strip()
            
        context += response + "\n"
        
        # Extract Thought for display
        thought_match = re.search(r"Thought:(.*?)(Action:|Answer:)", response, re.DOTALL)
        if thought_match:
            thought = thought_match.group(1).strip()
            print(f"THINK: {thought}")
            
        # Check if the agent reached the final answer
        if "Answer:" in response:
            answer = response.split("Answer:")[1].strip()
            print(f"FINAL ANSWER: {answer}\n")
            return
            
        # Extract Action
        action_match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
        
        if action_match:
            tool_name = action_match.group(1)
            args_str = action_match.group(2)
            print(f"ACT: Executing '{tool_name}' with arguments: ({args_str})")
            
            # 2. OBSERVE (Execute the tool and get the result)
            args = parse_args(args_str)
            if tool_name in TOOLS:
                try:
                    observation = TOOLS[tool_name](*args) if isinstance(args, tuple) else TOOLS[tool_name](*args)
                except Exception as e:
                    observation = f"Error: Tool execution failed: {e}"
            else:
                observation = f"Error: Tool {tool_name} not found."
                
            print(f"OBSERVE: {observation}\n")
            context += f"Observation: {observation}\n"
        else:
            print("ACT: Error - Invalid format. No valid action or answer found.\n")
            context += "Observation: Error: Invalid format. Please use 'Action: tool_name(args)' or 'Answer: final_answer'.\n"

    print("Failed to find an answer within the iteration limit.")

if __name__ == "__main__":
    questions = [
        "What is the GDP of India in USD, converted to INR?",
        "If a product costs $150 and there is a 18% GST, what is the final price in INR?",
        "How many days are there between January 15, 2025 and August 20, 2026?"
    ]
    
    for idx, q in enumerate(questions, 1):
        print("="*50)
        print(f"Processing Question {idx}")
        print("="*50)
        run_agent(q)
        print("\n")
