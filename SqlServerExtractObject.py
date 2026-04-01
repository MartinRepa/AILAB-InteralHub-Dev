import os
import re
import pyodbc

# -----------------------------
# CONFIG
# -----------------------------
OUTPUT_DIR = "sqlserver_exports"
SERVER = r"YOUR_SERVER"
DATABASE = "YOUR_DATABASE"
USERNAME = "YOUR_USERNAME"      # optional if using SQL auth
PASSWORD = "YOUR_PASSWORD"      # optional if using SQL auth
USE_TRUSTED_CONNECTION = True   # set False if using SQL auth

EXCLUDED_SCHEMAS = {
    "sys",
    "INFORMATION_SCHEMA"
}

OBJECTS = {
    "VIEW": {
        "folder": "VIEW",
        "prefix": "VW_"
    },
    # You can enable these later if needed:
    # "PROCEDURE": {
    #     "folder": "PROCEDURE",
    #     "prefix": "SP_"
    # },
    # "FUNCTION": {
    #     "folder": "FUNCTION",
    #     "prefix": "FN_"
    # }
}

# -----------------------------
# HELPERS
# -----------------------------
def safe_name(name: str) -> str:
    """
    Windows-safe file name.
    Keeps letters, digits, underscore, dash, dot.
    Replaces everything else with underscore.
    """
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def get_connection():
    if USE_TRUSTED_CONNECTION:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            "Trusted_Connection=yes;"
        )
    else:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
        )
    return pyodbc.connect(conn_str)


def ensure_create_uses_schema(ddl: str, object_type: str, schema_name: str, object_name: str) -> str:
    """
    Rewrites the first CREATE statement so that object name becomes schema.object_name
    if schema is missing in the definition.
    """

    if object_type == "VIEW":
        pattern = rf"(?is)(create\s+view\s+)(\[?{re.escape(object_name)}\]?)"
        replacement = rf"\1[{schema_name}].[{object_name}]"
        return re.sub(pattern, replacement, ddl, count=1)

    elif object_type == "PROCEDURE":
        pattern = rf"(?is)(create\s+procedure\s+)(\[?{re.escape(object_name)}\]?)"
        replacement = rf"\1[{schema_name}].[{object_name}]"
        return re.sub(pattern, replacement, ddl, count=1)

    elif object_type == "FUNCTION":
        pattern = rf"(?is)(create\s+function\s+)(\[?{re.escape(object_name)}\]?)"
        replacement = rf"\1[{schema_name}].[{object_name}]"
        return re.sub(pattern, replacement, ddl, count=1)

    return ddl


def fetch_objects(cursor, object_type: str):
    """
    Return rows as:
    (schema_name, object_name, object_id)
    """
    if object_type == "VIEW":
        sql = """
        SELECT
            s.name AS schema_name,
            v.name AS object_name,
            v.object_id
        FROM sys.views v
        INNER JOIN sys.schemas s
            ON v.schema_id = s.schema_id
        WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, v.name;
        """
    elif object_type == "PROCEDURE":
        sql = """
        SELECT
            s.name AS schema_name,
            p.name AS object_name,
            p.object_id
        FROM sys.procedures p
        INNER JOIN sys.schemas s
            ON p.schema_id = s.schema_id
        WHERE s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, p.name;
        """
    elif object_type == "FUNCTION":
        sql = """
        SELECT
            s.name AS schema_name,
            o.name AS object_name,
            o.object_id
        FROM sys.objects o
        INNER JOIN sys.schemas s
            ON o.schema_id = s.schema_id
        WHERE o.type IN ('FN', 'IF', 'TF')
          AND s.name NOT IN ('sys', 'INFORMATION_SCHEMA')
        ORDER BY s.name, o.name;
        """
    else:
        raise ValueError(f"Unsupported object_type: {object_type}")

    cursor.execute(sql)
    return cursor.fetchall()


def fetch_definition(cursor, object_id: int):
    sql = "SELECT OBJECT_DEFINITION(?)"
    cursor.execute(sql, object_id)
    row = cursor.fetchone()
    return row[0] if row and row[0] else None


# -----------------------------
# MAIN
# -----------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = get_connection()
cur = conn.cursor()

# Counters reset per (schema, object_type)
counters = {}

for object_type, cfg in OBJECTS.items():
    print(f"Exporting {object_type}...")

    rows = fetch_objects(cur, object_type)

    for row in rows:
        schema_name = str(row[0])
        object_name = str(row[1])
        object_id = int(row[2])

        if schema_name.upper() in {x.upper() for x in EXCLUDED_SCHEMAS}:
            continue

        print(f"{DATABASE}.{schema_name}.{object_name}")

        ddl = fetch_definition(cur, object_id)
        if not ddl:
            print(f"Skipping {schema_name}.{object_name} - no definition found.")
            continue

        ddl = ddl.strip()
        ddl = ensure_create_uses_schema(ddl, object_type, schema_name, object_name)

        key = (schema_name, object_type)
        counters.setdefault(key, 1)
        idx = counters[key]

        schema_dir = os.path.join(OUTPUT_DIR, safe_name(schema_name))
        object_dir = os.path.join(schema_dir, cfg["folder"])
        os.makedirs(object_dir, exist_ok=True)

        filename = f"{cfg['prefix']}{idx:03d}_{safe_name(object_name)}.sql"
        filepath = os.path.join(object_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(ddl)
            f.write("\n")

        counters[key] += 1

cur.close()
conn.close()

print("Export completed.")

def fetch_table_definition(cursor, schema_name: str, table_name: str) -> str:
    sql = """
    SELECT
        c.column_id,
        c.name AS column_name,
        typ.name AS data_type,
        c.max_length,
        c.precision,
        c.scale,
        c.is_nullable,
        c.is_identity,
        ic.seed_value,
        ic.increment_value,
        dc.definition AS default_definition
    FROM sys.columns c
    INNER JOIN sys.tables t
        ON c.object_id = t.object_id
    INNER JOIN sys.schemas s
        ON t.schema_id = s.schema_id
    INNER JOIN sys.types typ
        ON c.user_type_id = typ.user_type_id
    LEFT JOIN sys.identity_columns ic
        ON c.object_id = ic.object_id
       AND c.column_id = ic.column_id
    LEFT JOIN sys.default_constraints dc
        ON c.default_object_id = dc.object_id
    WHERE s.name = ?
      AND t.name = ?
    ORDER BY c.column_id;
    """
    cursor.execute(sql, schema_name, table_name)
    rows = cursor.fetchall()

    if not rows:
        return None

    column_lines = []

    for row in rows:
        (
            column_id,
            column_name,
            data_type,
            max_length,
            precision,
            scale,
            is_nullable,
            is_identity,
            seed_value,
            increment_value,
            default_definition
        ) = row

        data_type_upper = str(data_type).upper()

        if data_type_upper in ("VARCHAR", "CHAR", "VARBINARY", "BINARY"):
            if max_length == -1:
                type_def = f"{data_type_upper}(MAX)"
            else:
                type_def = f"{data_type_upper}({max_length})"

        elif data_type_upper in ("NVARCHAR", "NCHAR"):
            if max_length == -1:
                type_def = f"{data_type_upper}(MAX)"
            else:
                type_def = f"{data_type_upper}({max_length // 2})"

        elif data_type_upper in ("DECIMAL", "NUMERIC"):
            type_def = f"{data_type_upper}({precision},{scale})"

        elif data_type_upper in ("DATETIME2", "DATETIMEOFFSET", "TIME"):
            type_def = f"{data_type_upper}({scale})"

        else:
            type_def = data_type_upper

        col_def = f"[{column_name}] {type_def}"

        if is_identity:
            seed = int(seed_value) if seed_value is not None else 1
            inc = int(increment_value) if increment_value is not None else 1
            col_def += f" IDENTITY({seed},{inc})"

        if default_definition:
            col_def += f" DEFAULT {default_definition}"

        col_def += " NULL" if is_nullable else " NOT NULL"
        column_lines.append(col_def)

    ddl = (
        f"CREATE TABLE [{schema_name}].[{table_name}] (\n    " +
        ",\n    ".join(column_lines) +
        "\n);"
    )

    return ddl


ddl = fetch_definition(cur, object_id)
        if not ddl:
            print(f"Skipping {schema_name}.{object_name} - no definition found.")
            continue

        ddl = ddl.strip()
        ddl = ensure_create_uses_schema(ddl, object_type, schema_name, object_name)

if object_type == "TABLE":
            ddl = fetch_table_definition(cur, schema_name, object_name)
        else:
            ddl = fetch_definition(cur, object_id)
            if ddl:
                ddl = ddl.strip()
                ddl = ensure_create_uses_schema(ddl, object_type, schema_name, object_name)

        if not ddl:
            print(f"Skipping {schema_name}.{object_name} - no definition found.")
            continue


pyodbc.ProgrammingError: ('ODBC SQL type -150 is not yet supported.  column-index=8  type=-150', 'HY106')
