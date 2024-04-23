# Streamlit frontend to query, analyze the implied relational diagram and showcase a visual table & the possibility of CSV/xlsx export

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Function to create a connection to your SQL database
def get_connection():
    # Replace 'your_database_url' with your actual database connection URL or connection string
    return create_engine('your_database_url')

# Function to execute the SQL query and clean the DataFrame from leading/trailing spaces
@st.cache
def run_query(query):
    engine = get_connection()
    with engine.connect() as conn:
        result = pd.read_sql_query(query, conn)
        # Trim spaces from string columns
        for col in result.select_dtypes(include=['object']):  # 'object' usually means string in pandas
            result[col] = result[col].str.strip()
        return result

def main():
    st.title('SQL Query and Export to Excel Tool')
    
    # Text area for user to input SQL query
    query = st.text_area(
        "Write a SQL sentence:",
        value="""SELECT e.*, d.department_name, STRING_AGG(p.project_name, ', ' ORDER BY p.project_name) AS project_names, STRING_AGG(p.start_date::text, ', '
        ORDER BY p.start_date) AS project_start_dates, STRING_AGG(p.end_date::text, ', ' ORDER BY p.end_date) AS project_end_dates
        FROM employees e JOIN departments d ON e.department_id = d.department_id LEFT JOIN projects p ON d.department_id = p.department_id
        GROUP BY e.employee_id, d.department_id ORDER BY e.last_name, e.first_name;
        """,
        height=150,
    )

        # Provide download button if DataFrame is not empty
        if not df.empty and st.button('Export to Excel'):
            # Export DataFrame to Excel
            output = f"{pd.Timestamp('now').strftime('%Y-%m-%d_%H-%M-%S')}_output.xlsx"
            df.to_excel(output, index=False)
            st.success(f'Exported to {output}')

if __name__ == "__main__":
    main()