# Streamlit frontend to query, analyze the implied relational diagram and showcase a visual table & the possibility of CSV/xlsx export

import streamlit as st
import pandas as pd
import sqlparse
import io

# import connection parameters
from src.DBConnect import get_connection

# Import the refactored functions
from src.functions import extract_tables, generate_graphviz_dot

# Streamlit app setup
st.set_page_config(layout="wide")
st.header(":bar_chart: Example SQL querying, Relational Map & live interaction :bar_chart:")

# Creating columns with custom spacing and borders
col1, col2 = st.columns([0.4, 0.6])

# Adding a container to each column for better border control
col1_container = col1.container(border=True)
col2_container = col2.container(border=True)

with col1_container:
    # User input for SQL query
    query = st.text_area(
        "Write a SQL sentence:",
        value="""SELECT e.*, d.department_name, STRING_AGG(p.project_name, ', ' ORDER BY p.project_name) AS project_names, STRING_AGG(p.start_date::text, ', '
        ORDER BY p.start_date) AS project_start_dates, STRING_AGG(p.end_date::text, ', ' ORDER BY p.end_date) AS project_end_dates
        FROM employees e JOIN departments d ON e.department_id = d.department_id LEFT JOIN projects p ON d.department_id = p.department_id
        GROUP BY e.employee_id, d.department_id ORDER BY e.last_name, e.first_name;
        """,
        height=150,
    )

    if st.button("Execute query"):
        # Pre-process the query to remove trailing semicolons
        processed_query = query.rstrip(";")

        # Use the get_connection function to connect to the database
        with get_connection() as conn:
            try:
                # Executing the processed query
                df = pd.read_sql(processed_query, conn)

                # Format the SQL query for display
                formatted_query = sqlparse.format(
                    processed_query, reindent=True, keyword_case="upper"
                )
                # Displaying results in the first column
                col1_container.write("Query results:")
                col1_container.dataframe(df)

                # Extract tables from the query and generate a DOT string for visualization
                tables, joins = extract_tables(processed_query)
                dot_string = generate_graphviz_dot(tables, joins)

                # Render the relational map in the right column
                col2_container.write("Implied relational diagram:")
                col2_container.graphviz_chart(dot_string, use_container_width=False)
                # Moved inside try-except to only display after successful query execution
                col2_container.write("Formatted SQL query:")
                col2_container.code(formatted_query, language="sql")

                # Exporting results to Excel and adding SQL query as a comment to the first cell
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Results")
                    workbook = writer.book
                    worksheet = writer.sheets["Results"]
                    worksheet.write_comment(
                        "A1",
                        "Query: " + formatted_query,
                        {"visible": True, "author": "SQL Query"},
                    )
                    worksheet.set_column("A:A", 20)

                output.seek(0)  # Rewind the buffer

                # Download button for exporting results
                col2_container.download_button(
                    label="Download xlsx file",
                    data=output,
                    file_name="query_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            except Exception as e:
                st.error(f"There was an error: {e}")
