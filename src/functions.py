import re


def extract_tables(sql):
    """
    Extract table names, aliases, and JOIN conditions from the SQL query.
    Improvements to include all joined tables and handle their aliases and join conditions.
    """
    # Normalize and remove string literals for simplicity
    sql_no_strings = re.sub(r"'.*?'", "", sql, flags=re.DOTALL)
    # Match tables and aliases in FROM and JOIN clauses, and also catch the JOIN conditions
    regex = r"""
        \bFROM\b\s+(\w+)(\s+AS\s+|\s+)?(\w+)?|   # FROM clause with optional AS for alias
        \bJOIN\b\s+(\w+)(\s+AS\s+|\s+)?(\w+)?\s+ # JOIN clause with optional AS for alias
        (?:ON\s+(\w+\.\w+)\s*=\s*(\w+\.\w+))?    # ON JOIN conditions
    """
    matches = re.findall(regex, sql_no_strings, re.IGNORECASE | re.VERBOSE)

    tables = {}
    joins = []

    for (
        from_table,
        _,
        from_alias,
        join_table,
        _,
        join_alias,
        on_left,
        on_right,
    ) in matches:
        table_name = from_table or join_table
        alias = from_alias or join_alias or table_name
        if table_name:
            tables[alias] = table_name
        if on_left and on_right:
            joins.append(
                (
                    on_left.split(".")[0],
                    on_right.split(".")[0],
                    f"{on_left} = {on_right}",
                )
            )

    return tables, joins


def generate_graphviz_dot(tables, joins):
    """
    Generate a DOT string for Graphviz visualization from tables and their join conditions.
    """
    dot_string = "digraph SQL_Query {\n"
    for alias, table in tables.items():
        dot_string += f'  "{alias}" [label="{table} ({alias})"];\n'
    for left_table, right_table, condition in joins:
        # Ensure both sides of the join are in the tables list (by alias or actual name)
        left_alias = next(
            (
                alias
                for alias, t in tables.items()
                if t == left_table or alias == left_table
            ),
            None,
        )
        right_alias = next(
            (
                alias
                for alias, t in tables.items()
                if t == right_table or alias == right_table
            ),
            None,
        )
        if left_alias and right_alias:
            dot_string += (
                f'  "{left_alias}" -> "{right_alias}" [label="{condition}"];\n'
            )
    dot_string += "}\n"
    return dot_string
