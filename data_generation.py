import json
import pandas as pd
from google import genai
from google.genai import types

# FORCE location to us-central1 where the model lives
client = genai.Client(vertexai=True, project='gd-gcp-gridu-genai', location='us-central1')

def generate_synthetic_data(ddl_schema, num_rows, custom_instructions, temperature):
    """
    Generates data based on Schema + User Instructions + Temperature.
    """
    prompt = f"""
    You are a synthetic data generator. 
    1. Analyze the following SQL DDL schema:
    {ddl_schema}
    
    2. User Instructions for the data: "{custom_instructions}"
    
    3. Generate {num_rows} rows of realistic synthetic data for this table.
    4. Return ONLY a valid JSON array of objects. Keys must match column names.
    5. Do not include markdown formatting like ```json.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=temperature  # Use the slider value
            )
        )
        data = json.loads(response.text)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error generating data: {e}")
        return pd.DataFrame()

def refine_data(current_df, edit_instructions):
    """
    Takes existing data and applies changes based on user text.
    """
    # Convert current data to JSON to send to AI
    data_json = current_df.to_json(orient='records')
    
    prompt = f"""
    You are a data editor.
    1. Current Data (JSON):
    {data_json}
    
    2. User Edit Instructions: "{edit_instructions}"
    
    3. Task: Apply the changes to the data and return the updated JSON.
    4. Return ONLY valid JSON array.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        data = json.loads(response.text)
        return pd.DataFrame(data)
    except Exception as e:
        return current_df