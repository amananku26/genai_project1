from google import genai
from google.genai import types
from pandasql import sqldf

# FORCE location to us-central1 where the model lives
client = genai.Client(vertexai=True, project='gd-gcp-gridu-genai', location='us-central1')

def text_to_sql(user_question, table_name, columns):
    schema_context = f"Table Name: {table_name}, Columns: {', '.join(columns)}"
    prompt = f"""
    You are an expert SQL translator.
    1. Context: {schema_context}
    2. User Question: "{user_question}"
    3. Task: Generate a valid SQL query (SQLite syntax).
    4. Return ONLY the SQL query. No markdown.
    """
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt
    )
    return response.text.strip().replace("```sql", "").replace("```", "")

def execute_sql_on_dataframe(df, sql_query):
    my_table = df 
    try:
        return sqldf(sql_query, locals())
    except Exception as e:
        return f"Error executing SQL: {e}"
