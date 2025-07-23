from fastapi import FastAPI
from pydantic import BaseModel
from agent.database import get_db_connection
from agent.llm import get_sql_query
from agent.visuals1 import generate_bar_chart
import pandas as pd

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query/")
def query_agent(request: QueryRequest):
    sql_query = get_sql_query(request.question)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        result = [dict(zip(columns, row)) for row in rows]

        response = {"answer": result}

        # Only generate chart if there are at least 2 columns and data is not empty
        if len(columns) >= 2 and len(result) > 0:
            chart_data = generate_bar_chart(result, columns[:2])
            response["visual"] = chart_data
        else:
            response["visual"] = "Bar chart requires exactly 2 columns in result and non-empty data."

        return response

    except Exception as e:
        return {"detail": f"SQL Error: {str(e)}"}
    
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)