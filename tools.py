import json
from datetime import datetime

def web_search(query: str) -> str:
    """
    Simulates a web search using a local JSON file.
    In a real agent, this would call an API like Google Custom Search or Serper.
    """
    try:
        # Load our mock "internet"
        with open('search_data.json', 'r') as f:
            data = json.load(f)
        
        # Clean up the query so it's easier to match
        query_lower = query.lower()
        query_words = set(query_lower.replace(',', '').replace('?', '').split())
        
        # Look through our mock internet to see if any keys match the user's search
        for k, results_list in data.items():
            key_words = set(k.lower().split())
            
            # If the search query contains our key words, return the results
            if key_words.issubset(query_words) or k in query_lower or query_lower in k:
                
                # Format the search results into a clean text string
                formatted_response = ""
                for idx, res in enumerate(results_list, 1):
                    formatted_response += f"Result {idx}:\n"
                    formatted_response += f"Title: {res.get('title')}\n"
                    formatted_response += f"URL: {res.get('url')}\n"
                    formatted_response += f"Snippet: {res.get('snippet')}\n\n"
                    
                return formatted_response.strip()
                
        return "Search returned no results."
    except Exception as e:
        return f"Error: {e}"

def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression safely.
    When the agent needs to do math, it builds a string (like "10 * 5") and passes it here.
    """
    try:
        # Note for students: eval() can be dangerous if running untrusted code!
        # Passing {"__builtins__": None} prevents the agent from running harmful Python commands
        # like deleting files, restricting it strictly to basic math.
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error in calculation: {e}"

def get_exchange_rate(currency: str) -> str:
    """
    Returns exchange rate for a given currency relative to USD.
    In a real app, this would make an API call to a live currency converter.
    """
    # Hardcoded fallback rates for demonstration purposes
    rates = {
        "INR": 83.0,
        "EUR": 0.92,
        "GBP": 0.78
    }
    
    # Standardize the input (e.g. "inr" -> "INR")
    currency = currency.upper().strip()
    return str(rates.get(currency, "Rate not found"))

def date_difference(date1_str: str, date2_str: str) -> str:
    """
    Computes difference in days between two dates.
    The agent must format its strings EXACTLY as "Month DD, YYYY" for this to work.
    """
    try:
        # Convert the string dates into Python datetime objects
        d1 = datetime.strptime(date1_str.strip(), "%B %d, %Y")
        d2 = datetime.strptime(date2_str.strip(), "%B %d, %Y")
        
        # Calculate the absolute difference in days
        return str(abs((d2 - d1).days))
    except Exception as e:
        return f"Error parsing dates: {e}. Remember to format as 'Month DD, YYYY'."

# Dictionary mapping string tool names to actual Python functions.
# This allows the agent to call tools dynamically by printing their names!
TOOLS = {
    "web_search": web_search,
    "calculator": calculator,
    "get_exchange_rate": get_exchange_rate,
    "date_difference": date_difference
}
