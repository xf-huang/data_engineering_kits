import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
import pandas as pd

class DataQuaINS:
    def __init__(self):
        self.input_file_path = ""
        self.out_file_path = ""
        self.host = ""
        self.database = ""
        self.user = ""
        self.password = ""
        self.port = ""

# 建立连接
    def connection(self):
        db_params = {
            'host': self.host,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'port': self.port
        }

        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        return connection

    # 读取表名列表，质检表格数据并将质检结果写入excel文件中
    def data_qual_insp(self):
        connection = self.connection()
        cursor = connection.cursor(cursor_factory=DictCursor)
        tb_list = pd.read_excel(self.input_file_path)["表名"].to_list()
        tb_name_list = pd.read_excel(self.input_file_path)["别名"].to_list()
        inspect_results_list = []
        for tb, alias in zip(tb_list, tb_name_list):
            try:
                # 获取表格字段名称
                columns_name_query = sql.SQL(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tb}';")
                cursor.execute(columns_name_query)
                column_list = [table[0] for table in cursor.fetchall()]
                if len(column_list)>0:
                    # 获取字段数据类型
                    columns_type_query = sql.SQL(
                        f"SELECT data_type FROM information_schema.columns WHERE table_name = '{tb}';")
                    cursor.execute(columns_type_query)
                    column_datatype = [table[0] for table in cursor.fetchall()]
                    # 是否是矢量数据
                    if "smgeometry" in column_list:
                        is_vector = "是"
                        # 获取矢量类型
                        vector_type_query = f"SELECT ST_GeometryType(smgeometry) FROM {tb} LIMIT 1;"
                        cursor.execute(vector_type_query)
                        vector_type = cursor.fetchone()[0]
                        # 矢量类型
                        if vector_type == 'ST_Point':
                            shape = "点"
                        elif vector_type == 'ST_MultiLineString':
                            shape = "线"
                        elif vector_type == 'ST_MultiPolygon':
                            shape = "面"
                        else:
                            shape = ""
                    else:
                        is_vector = "否"
                        shape = ""

                    # 有无数据标识码字段
                    if "ocean_data_identification_code" in column_list:
                        has_bsm = "有"
                    else:
                        has_bsm = "无"

                    # 有无时间日期字段
                    if "timestamp with time zone" in column_datatype:
                        has_dt = "有"
                    else:
                        has_dt = "无"

                    # 最小线长度
                    if shape == "线":
                        min_line_query = f"SELECT MIN(smlength) FROM {tb}"
                        cursor.execute(min_line_query)
                        min_la = cursor.fetchone()[0]
                    elif shape == "面":
                        min_area_query = f"SELECT MIN(smarea) FROM {tb}"
                        cursor.execute(min_area_query)
                        min_la = cursor.fetchone()[0]
                    else:
                        min_la = ""

                    result = [alias, is_vector, shape, min_la, has_bsm, has_dt]
                    inspect_results_list.append(result)
                    #print(tb, result)
                else:
                    print(f"{tb} 在数据库中不存在")
                    continue
            except Exception as e:
                print(str(e))
                continue
        # 输出质检结论
        df_results = pd.DataFrame(inspect_results_list, columns=["数据名称", "是否矢量", "矢量类型", "最小线/面", "有无数据标识码", "有无时间字段"])
        df_results.to_excel(self.out_file_path, index=False)

        # Close the cursor and connection
        cursor.close()
        connection.close()

# 测试
if __name__ == "__main__":
    test_instance = DataQuaINS()
    test_instance.input_file_path = "./测试数据/pg库表名.xlsx"
    #test_instance.out_file_path = "./测试数据/导出表格元数据"
    test_instance.out_file_path = "./测试数据/质检结论.xlsx"


    test_instance.host = 'localhost'
    test_instance.database = 'pg_test'
    test_instance.user = 'postgres'
    test_instance.password = '314159'
    test_instance.port = '5432'

    # test_instance.get_tables_meta_data()
    test_instance.data_qual_insp()
