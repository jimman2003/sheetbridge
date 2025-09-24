import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
import dotenv
import ollama
from openai import OpenAI
from traditional.utils import time_function

dotenv.load_dotenv()

system_prompt_formula = """
Act as an expert at converting Excel formulas to Python Pandas code. Input will be SpreadsheetML XML exported from an Excel worksheet. Automatically parse the XML, extract each cell’s formula from <f> elements (including shared or array formulas if present), and produce equivalent, runnable Python code that uses Pandas for each formula. For each item:
•	Generate Python code that mirrors the Excel logic, including operators, function semantics, ranges, and absolute/relative references.
•	If ranges are used (e.g., A1:A10), translate them into Python data access patterns and aggregate operations.
•	Note any Excel functions without direct Python equivalents and propose idiomatic alternatives.
•	Provide a brief explanation of how the Python code implements the formula.
Assumptions:
•	SpreadsheetML stores formulas in the CellFormula element <f> for cells with formulas.
•	The workbook structure follows the Open XML SpreadsheetML specification.
•	If a formula is shared, resolve the base formula and adjust cell-relative references for each dependent cell.
Return a structured list of results for all formulas found.

"""



class FormulaResponse(BaseModel):
    formula: str = Field(..., description="The generated formula as a string.")
    explanation: str = Field(..., description="A brief explanation of the formula.")


gemini_client = genai.Client()
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@time_function("Gemini API")
def generate_formula_gemini(system_prompt: str, user_prompt: str):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=list[FormulaResponse],
        ),
    )
    return response.parsed


@time_function("Ollama API")
def generate_formula_ollama(system_prompt: str, user_prompt: str):
    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        format=FormulaResponse.model_json_schema(),
    )
    # Assuming the response content is a JSON string that can be parsed into FormulaResponse
    return FormulaResponse.model_validate_json(response.message.content)


@time_function("OpenRouter API")
def generate_formula_openrouter(system_prompt: str, user_prompt: str):
    response = openrouter_client.chat.completions.create(
        model="deepseek/deepseek-chat-v3.1:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        # response_format={"type":"json_schema", "json_schema": FormulaResponse.model_json_schema()},
    )
    return response.choices[0].message.content
