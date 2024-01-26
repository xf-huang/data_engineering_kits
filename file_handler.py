import pandas as pd


class FileHandler:
    def __init__(self):
        self.input_file_path = ""  # 输入文件路径
        self.output_file_path = ""  # 输出文件路径
        self.address_column_name = ""  # 地址列名
        self.name_column_name = ""  # 单位名称列名
        self.input_df = ""
        self.output_df = pd.DataFrame()  # 导出文件

    # 读取表格
    def read_table(self):
        if self.input_file_path.endswith(".xlsx") or self.input_file_path.endswith(".xls"):
            table = pd.read_excel(self.input_file_path)
            self.input_df = table
        elif self.input_file_path.endswith(".csv"):
            table = pd.read_csv(self.input_file_path)
            self.input_df = table
        return table

    # 获取表格文件表头
    def get_column_names(self):
        if self.input_file_path.endswith(".xlsx") or self.input_file_path.endswith(".xls"):
            table = pd.read_excel(self.input_file_path, nrows=1)
        elif self.input_file_path.endswith(".csv"):
            table = pd.read_csv(self.input_file_path, nrows=1)
        column_names = table.columns.to_list()
        return column_names

    # 导出表格
    def write_table(self):
        if self.output_file_path.endswith(".xlsx") or self.input_file_path.endswith(".xls"):
            self.output_df.to_excel(self.output_file_path, index=False)
        elif self.output_file_path.endswith(".csv"):
            self.output_df.to_csv(self.output_file_path, index=False)


if __name__ == "__main__":
    file_handler = FileHandler()
    file_handler.input_file_path = "D:\\Documents\\工作\\数据\\test.csv"
    file_handler.output_file_path = "D:\\Documents\\工作\\数据\\test_output.csv"
    column_names = file_handler.get_column_names()
    print(column_names)
    df = file_handler.read_table()
    file_handler.output_df = df
    file_handler.write_table()

