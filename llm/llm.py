import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
import dotenv
import ollama
from openai import OpenAI

dotenv.load_dotenv()
system_prompt_formula = """
You are an expert in creating Python code from spreadsheet formulas. 
Given the Excel formula, generate the appropriate Python code and provide a brief explanation of how it works.
"""



class FormulaResponse(BaseModel):
    formula: str = Field(..., description="The generated formula as a string.")
    explanation: str = Field(..., description="A brief explanation of the formula.")


gemini_client = genai.Client()
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_formula_gemini(system_prompt: str, user_prompt: str):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=FormulaResponse,
        ),
    )
    return response


def generate_formula_ollama(system_prompt: str, user_prompt: str):
    response = ollama.chat(
        model="qwen2.5-7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        format=FormulaResponse.model_json_schema(),
    )
    # Assuming the response content is a JSON string that can be parsed into FormulaResponse
    return FormulaResponse.model_validate_json(response.message.content)


def generate_formula_openrouter(system_prompt: str, user_prompt: str):
    response = openrouter_client.chat.completions.create(
        model="deepseek/deepseek-chat-v3.1:free",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type":"json_schema", "json_schema": FormulaResponse.model_json_schema()},
    )
    return response
