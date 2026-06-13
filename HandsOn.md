# Bonus Tutorial: Mastering ReAct with Tool Chaining

Welcome to the advanced section of the ReAct Agent assignment! Now that you have built the core `Observe -> Think -> Act` loop, we are going to explore one of the most powerful concepts in agentic AI: **Tool Chaining**.

Tool chaining is when an agent uses the **Observation** (output) of one tool as the **Action argument** (input) for the next tool.

## The Goal
Currently, Question 3 is: 
*"How many days are there between January 15, 2025 and August 20, 2026?"*

This is a simple one-step problem. The agent just calls the `date_difference` tool. Let's make it more realistic. We are going to change Question 3 to:

> *"How many days are there between **today** and August 20, 2026?"*

---

### 🧠 Intuitive Question 1
> **Before writing any code, think about this:** 
> If the agent reads the word "today" in the prompt, what information is it missing? Can the existing `date_difference` tool solve this problem on its own? Why or why not?

*(Hint: Does the agent inherently know what the current date is?)*

---

To solve this, we need to give the agent a way to find out what "today" is *before* it tries to calculate the difference. Follow these steps to implement the changes.

## Step 1: Create the `get_today_date` function

**File to modify:** `tools.py`

Open `tools.py` and add a new Python function that returns the current date. Make sure it returns the date in the exact same format that the `date_difference` tool expects (`Month DD, YYYY`).

Add this code above the `TOOLS` dictionary:

```python
from datetime import datetime

def get_today_date() -> str:
    """Returns today's date in 'Month DD, YYYY' format."""
    return datetime.now().strftime("%B %d, %Y")
```

---

### 🧠 Intuitive Question 2
> **Look at the code above:** 
> Why is it so important that we use `.strftime("%B %d, %Y")`? What would happen if our new tool returned `"2026-06-13"` and the agent passed that directly into the `date_difference` tool? 

*(Hint: Look at how `date_difference` parses the strings passed into it in `tools.py`.)*

---

## Step 2: Register the New Tool

**File to modify:** `tools.py`

Your agent won't know the Python function exists unless you map it in the `TOOLS` dictionary at the bottom of the file.

Update the dictionary to look like this:

```python
# Map tool names to functions
TOOLS = {
    "web_search": web_search,
    "calculator": calculator,
    "get_exchange_rate": get_exchange_rate,
    "date_difference": date_difference,
    "get_today_date": get_today_date      # <-- Add this new line!
}
```

## Step 3: Update the System Prompt

**File to modify:** `main.py`

We have created the code for the tool, but the LLM still doesn't know it has permission to use it. We must update the instructions.

Find the `SYSTEM_PROMPT` variable at the top of `main.py` and add the new tool as option #5:

```python
SYSTEM_PROMPT = """You are an advanced reasoning agent designed to solve problems using a multi-step ReAct (Reason + Act) loop.

You have access to the following tools:
1. web_search(query: str) - Retrieves facts from a search engine.
2. calculator(expression: str) - Evaluates a mathematical expression (e.g. 150 * 1.18).
3. get_exchange_rate(currency: str) - Returns the exchange rate for a given currency relative to USD (e.g. INR).
4. date_difference(date1: str, date2: str) - Returns the number of days between two dates formatted as "Month DD, YYYY".
5. get_today_date() - Returns the current date in "Month DD, YYYY" format. Use this when you need to know today's date.

... (keep the rest of the prompt the same) ...
"""
```

## Step 4: Change the Question

**File to modify:** `main.py`

Finally, go to the bottom of `main.py` where the `questions` list is defined, and modify the third question to challenge the agent.

```python
    questions = [
        "What is the GDP of India in USD, converted to INR?",
        "If a product costs $150 and there is a 18% GST, what is the final price in INR?",
        "How many days are there between today and August 20, 2026?" # <-- Update this line
    ]
```

---

## What to Expect (The Output Trace)

Run your agent! `python main.py`

If implemented correctly, your agent's thought process for Question 3 should now look something like this:

```text
THINK: I need to calculate the difference in days between today and August 20, 2026. First, I need to know today's date.
ACT: Executing 'get_today_date' with arguments: ()
OBSERVE: June 13, 2026

THINK: Now I know today is June 13, 2026. I can use the date_difference tool to calculate the days between June 13, 2026 and August 20, 2026.
ACT: Executing 'date_difference' with arguments: ('June 13, 2026', 'August 20, 2026')
OBSERVE: 68

FINAL ANSWER: There are 68 days between today and August 20, 2026.
```

### 🧠 Intuitive Question 3
> **Final thought:**
> Notice how the agent used the exact text `June 13, 2026` from the first Observation as an argument in its second Action. How does the ReAct framework technically make this possible? What part of your `main.py` loop ensures the LLM "remembers" the output of the first tool?

---
---

## Bonus Challenge 2: Search -> Read Chaining

A real-world AI agent doesn't just read short snippets from a search engine. It clicks on links to read the full context! Let's implement a `read_webpage` tool to force the agent to find a URL using `web_search` and then pass that exact URL into `read_webpage`.

### 🧠 Intuitive Question 4
> **Consider the search process:**
> If we ask the agent "What are the three key drivers of India's economy?", the `web_search` tool only gives a short snippet that might not contain the full answer. Why is it important for an agent to be able to dynamically pass URLs between tools, rather than having the developer hardcode the URL?

---

### Step 5: Add the `read_webpage` tool

**File to modify:** `tools.py`

Add this mock webpage reader tool above the `TOOLS` dictionary. This simulates what happens when an agent actually visits a specific URL to read the entire text.

```python
def read_webpage(url: str) -> str:
    """Reads the full content of a webpage given its URL."""
    mock_pages = {
        "https://www.economic-reports.com/india-gdp-latest": (
            "Full Report: India's economy is booming. The GDP is 4.15 trillion USD. "
            "The three key drivers of the economy are IT, agriculture, and manufacturing. "
            "Growth is expected to continue into the next decade."
        ),
        "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)": (
            "List of Countries: 1. USA - 31.8 trillion USD, 2. China - 18.53 trillion USD, ... "
            "5. India - 4.15 trillion USD."
        ),
        "https://www.economic-reports.com/usa-gdp-latest": (
            "USA Economic Report: The GDP has reached 31.8 trillion USD, maintaining its "
            "position as the largest economy driven by tech and services."
        )
    }
    # Return the content or a 404 error
    return mock_pages.get(url.strip(" '\""), "Error: 404 Page Not Found.")
```

### Step 6: Register the new tool

**File to modify:** `tools.py`

Don't forget to expose the tool to the system!

```python
# Map tool names to functions
TOOLS = {
    "web_search": web_search,
    "calculator": calculator,
    "get_exchange_rate": get_exchange_rate,
    "date_difference": date_difference,
    "get_today_date": get_today_date,
    "read_webpage": read_webpage      # <-- Add this!
}
```

### Step 7: Update the System Prompt

**File to modify:** `main.py`

Add option #6 to the `SYSTEM_PROMPT` in `main.py`:

```python
6. read_webpage(url: str) - Reads the full text content of a webpage. Requires a valid URL as the argument.
```

### Step 8: Update the First Question

**File to modify:** `main.py`

Change the very first question in the `questions` list to require deep reading, rather than a surface-level search:

```python
    questions = [
        "According to the latest economic reports, what are the three key drivers of India's economy?", # <-- Update this line
        "If a product costs $150 and there is a 18% GST, what is the final price in INR?",
        "How many days are there between today and August 20, 2026?"
    ]
```

---

## What to Expect (Search -> Read Trace)

When you run `python main.py` now, watch how the agent interacts with Question 1. It perfectly mirrors how a human browses the web!

```text
THINK: I need to find the latest economic reports about India's economy to identify its key drivers. I'll start with a web search.
ACT: Executing 'web_search' with arguments: ('India economy key drivers')
OBSERVE: Result 1:
Title: India GDP reaches new heights in recent estimates
URL: https://www.economic-reports.com/india-gdp-latest
Snippet: According to the latest global economic reports, the GDP of India currently stands at approximately 4.15 trillion USD...

THINK: The snippet doesn't explicitly list the three key drivers. I need to read the full report at the provided URL.
ACT: Executing 'read_webpage' with arguments: ('https://www.economic-reports.com/india-gdp-latest')
OBSERVE: Full Report: India's economy is booming. The GDP is 4.15 trillion USD. The three key drivers of the economy are IT, agriculture, and manufacturing. Growth is expected to continue into the next decade.

THINK: I now have the three key drivers of India's economy from the report.
FINAL ANSWER: According to the latest economic reports, the three key drivers of India's economy are IT, agriculture, and manufacturing.
```

### 🧠 Intuitive Question 5
> **Why this matters:**
> Notice that the `read_webpage` tool strictly takes a URL. Why couldn't the agent just call `read_webpage("India economy key drivers")`? What fundamental limitation of language models does this multi-step search-and-read process solve? 
> *(Hint: Think about how a browser works versus a search engine. Why do agents need both?)*
