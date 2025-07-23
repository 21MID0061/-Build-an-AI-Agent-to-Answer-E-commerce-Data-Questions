import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path=".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

PROMPT_TEMPLATE = '''
You are an expert data analyst. Given a user's question about e-commerce data, generate a valid SQLite SQL query to answer it. 
Only use the following tables and columns:

Table: ad_sales
- date (TEXT)
- item_id (INTEGER)
- ad_sales (REAL)
- impressions (INTEGER)
- ad_spend (REAL)
- clicks (INTEGER)
- units_sold (INTEGER)

Table: eligibility
- eligibility_datetime_utc (TEXT)
- item_id (INTEGER)
- eligibility (INTEGER)
- message (TEXT)

Return ONLY the SQL query, nothing else.

User question: {question}
'''

def get_sql_query(question: str) -> str:
   
    lower_q = question.lower()

    if "roas" in lower_q or "return on ad spend" in lower_q:
        return "SELECT item_id, SUM(ad_sales)/NULLIF(SUM(ad_spend), 0) AS roas FROM ad_sales GROUP BY item_id;"

    if "ad sales" in lower_q and "per item" in lower_q:
        return "SELECT item_id, SUM(ad_sales) AS total_ad_sales FROM ad_sales GROUP BY item_id;"

    if "clicks per item" in lower_q:
        return "SELECT item_id, SUM(clicks) AS total_clicks FROM ad_sales GROUP BY item_id;"

    if "units sold" in lower_q:
        return "SELECT item_id, SUM(units_sold) AS total_units_sold FROM ad_sales GROUP BY item_id;"

    prompt = PROMPT_TEMPLATE.format(question=question)

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    sql = response.choices[0].message.content.strip()

    if sql.startswith("```"):
        sql = sql.strip("`").replace("sql", "").strip()

    return sql
