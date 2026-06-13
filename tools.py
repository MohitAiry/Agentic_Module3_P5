import json
from datetime import datetime

def web_search(query: str) -> str:
    """Simulates a web search using a local JSON file."""
    try:
        with open('search_data.json', 'r') as f:
            data = json.load(f)
        
        query_lower = query.lower()
        query_words = set(query_lower.replace(',', '').replace('?', '').split())
        
        for k, results_list in data.items():
            key_words = set(k.lower().split())
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
    """Evaluates a mathematical expression safely."""
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error in calculation: {e}"

def get_exchange_rate(currency: str) -> str:
    """Returns exchange rate for a given currency."""
    rates = {
        "INR": 83.0,
        "EUR": 0.92,
        "GBP": 0.78
    }
    currency = currency.upper().strip()
    return str(rates.get(currency, "Rate not found"))

def date_difference(date1_str: str, date2_str: str) -> str:
    """Computes difference in days between two dates. Format: Month DD, YYYY"""
    try:
        d1 = datetime.strptime(date1_str.strip(), "%B %d, %Y")
        d2 = datetime.strptime(date2_str.strip(), "%B %d, %Y")
        return str(abs((d2 - d1).days))
    except Exception as e:
        return f"Error parsing dates: {e}"

# Map tool names to functions
TOOLS = {
    "web_search": web_search,
    "calculator": calculator,
    "get_exchange_rate": get_exchange_rate,
    "date_difference": date_difference
}
