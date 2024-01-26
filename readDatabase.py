import psycopg2
from psycopg2 import sql

# Replace these with your actual database connection details
db_params = {
    'host': '192.168.1.211',
    'database': 'gdf_tool',
    'user': 'gdf',
    'password': 'gdfadmin',
    'port': '5432'
}

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(**db_params)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# 获取字段名、别名、数据类型、是否主外键
metadata_query = sql.SQL("""
    SELECT
    a.attname AS column_name,
    d.description AS column_remark,
    format_type(a.atttypid, a.atttypmod) AS data_type,
    CASE
        WHEN con.contype = 'p' THEN '主'
        WHEN con.contype = 'f' THEN '外'
        ELSE NULL
    END AS key_type
FROM
    pg_attribute a
LEFT JOIN
    pg_description d ON a.attrelid = d.objoid AND a.attnum = d.objsubid
LEFT JOIN
    pg_constraint con ON con.conrelid = a.attrelid AND a.attnum = ANY(con.conkey)
WHERE
    a.attrelid = 'dwt_gd_coastal_nature_state_survey'::regclass
    AND a.attnum > 0
""")




cursor.execute(metadata_query)

# Fetch all the table names
#table_names = cursor.fetchall()

matadata_values = cursor.fetchall()
# Print the table names

metadata_values_list = []
for item in matadata_values:
    col_name = item[0]
    col_dp = item[2]
    #print(item)
    # 判断字段是否为空
    isnull_query = sql.SQL(f"""
        SELECT COUNT ({col_name}) = 0
        FROM dwt_gd_coastal_nature_state_survey;
    """)
    isnull = cursor.execute(isnull_query)
    isnull = cursor.fetchone()[0]
    if isnull == False:
        col_is_null = ""
    else:
        col_is_null = "空"
    # 获取字符字段的值域
    if col_name != 'id' and col_dp.startswith("character varying"):
        # 获取字段唯一值
        distinct_value_query = sql.SQL(f"""
            SELECT DISTINCT {col_name}
            FROM dwt_gd_coastal_nature_state_survey
        """)

        distinct_values = cursor.execute(distinct_value_query)
        distinct_values = cursor.fetchall()
        #print(distinct_values)
        if distinct_values[0][0]:
            distinct_values = "，".join([val[0] for val in distinct_values])
        else:
            distinct_values = ""
    else:
        distinct_values = ""
    item = item + (col_is_null, distinct_values)
    metadata_values_list.append(item)
print(metadata_values_list)
#print("，".join([a[0] for a in column_metadata]))



# Close the cursor and connection
cursor.close()
connection.close()
