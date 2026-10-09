
import os

from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY missing. Please check your .env file."
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_gemini(prompt):
    """Send a prompt to Gemini and return its response."""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    if response.text is None:
        raise ValueError(
            "Gemini returned an empty response. Please try again."
        )

    return response.text


def review_python_code(source_code):
    """Review Python code and suggest improvements using Gemini."""

    prompt = f'''
You are an experienced Python code reviewer.

Analyze the following Python source code.

Provide these sections:

1. CODE PURPOSE
Explain what the code does in simple language.

2. POTENTIAL BUGS
Identify possible bugs. Do not invent bugs.
If no obvious bugs are found, state that clearly.

3. CODE IMPROVEMENTS
Suggest specific improvements and explain why they help.

4. MISSING DOCUMENTATION
Identify functions and classes missing docstrings.
Write suitable docstring drafts for them.

5. BEST PRACTICES
Suggest relevant Python best practices.

Requirements:
- Keep the explanation beginner-friendly.
- Base your review on the supplied code.
- Do not claim the code was executed or tested.
- Do not modify the original source code.

Python source code:

```python
{source_code}
```
'''

    return ask_gemini(prompt)


def generate_ai_documentation(source_code):
    """Generate documentation drafts for Python code using Gemini."""

    prompt = f'''
You are an expert Python developer and technical writer.

Analyze the Python source code below.

Generate documentation drafts for every function,
asynchronous function, and class.

For each function, include:
- Purpose
- Parameters and types, when known
- Return value, when known
- Important exceptions or side effects, when applicable

For each class, include:
- Purpose and responsibilities
- Important attributes, when known
- Important methods, when known

Requirements:
- Write concise, meaningful Python docstrings.
- Use triple double quotes for each docstring.
- Do not invent behavior that is not supported by the code.
- Mark unknown details as unspecified instead of guessing.
- Show the function or class name before its draft.
- Do not rewrite or modify the original source code.
- If the code has no functions or classes, state that clearly.

Python source code:

```python
{source_code}
```
'''

    return ask_gemini(prompt)