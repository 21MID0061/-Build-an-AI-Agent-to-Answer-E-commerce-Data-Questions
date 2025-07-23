# agent/visuals1.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.database import get_db_connection
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def generate_bar_chart(data, columns):
    try:
        df = pd.DataFrame(data, columns=columns)

        if df.empty:
            return {"error": "No data to visualize."}

        if len(columns) < 2:
            return {"error": "Need at least two columns to plot."}

        x_col = columns[0]
        y_col = columns[1]

        df = df.sort_values(by=y_col, ascending=False)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df[x_col], df[y_col], color='skyblue')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} by {x_col}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        return {
            "chart_type": "bar_chart",
            "x": x_col,
            "y": y_col,
            "image_base64": image_base64,
            "message": f"Bar chart of {y_col} by {x_col}"
        }

    except Exception as e:
        return {"error": f"Chart generation failed: {str(e)}"}
