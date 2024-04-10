# Streamlit frontend to query, analyze the relational diagram and offer a visual table and the possibility of xlsx export

import streamlit as st
import pandas as pd
import sqlparse
import io

# import connection parameters
from src.DBConnect  import get_connection

# Import the refactored functions
from src.functions import extract_tables, generate_graphviz_dot

# Streamlit app setup
st.set_page_config(layout="wide")
st.header(":bar_chart: Example SQL, Excel & Relational Map :bar_chart:")

# Creating columns with custom spacing and borders
col1, col2 = st.columns([0.4, 0.6])

# Adding a container to each column for better border control
col1_container = col1.container(border=True)
col2_container = col2.container(border=True)


with col1_container:
    # User input for SQL query
    query = st.text_area(
        "Introduce la secuencia SQL a consultar",
        value="""
        SELECT employees.*, departments.department_name FROM employees
        INNER JOIN departments ON employees.department_id = departments.department_id;
        """,
        height=150,
    )

    if st.button("Ejecutar Consulta"):
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
                # Moved inside try-except to only display after successful query execution
                col1_container.write("Consulta SQL Formateada:")
                col1_container.code(formatted_query, language="sql")

                # Extract tables from the query and generate a DOT string for visualization
                tables, joins= extract_tables(processed_query)
                dot_string = generate_graphviz_dot(tables, joins)

                # Render the relational map in the right column
                col2_container.write("Diagrama relacional implicado:")
                col2_container.graphviz_chart(dot_string, use_container_width=True)

                # Displaying results in the second column
                col2_container.write("Resultados de la Consulta:")
                col2_container.dataframe(
                    df
                )  # Use dataframe instead of data_editor for broader compatibility

                # Exporting results to Excel and adding SQL query as a comment to the first cell
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Resultados")
                    workbook = writer.book
                    worksheet = writer.sheets["Resultados"]
                    worksheet.write_comment(
                        "A1",
                        "Query: " + formatted_query,
                        {"visible": True, "author": "SQL Query"},
                    )
                    worksheet.set_column("A:A", 20)

                output.seek(0)  # Rewind the buffer

                # Download button for exporting results
                col2_container.download_button(
                    label="Descargar Excel",
                    data=output,
                    file_name="resultados_consulta.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            except Exception as e:
                st.error(f"Se produjo un error: {e}")