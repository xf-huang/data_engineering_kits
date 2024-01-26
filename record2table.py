import os
import xlwings as xw
import pandas as pd


class Record2Table:
    def __init__(self):
        self.input_path = ""  # 输入的文件夹路径
        self.output_path = ""  # 输出的表格文件路径
        self.ref_table_path = ""  # 对应关系表格文件路径

    # 读取记录数据
    def read_records(self):
        # 新建一个app(相当于Excel软件)
        app = xw.App(visible=True, add_book=False)
        # 获取文件夹中的所有文件名
        file_names = os.listdir(self.input_path)
        # 读取对应关系表
        df_ref = pd.read_excel(self.ref_table_path)
        df_ref.dropna(how='all', inplace=True)
        all_records_list = []  # 汇总数据的总列表
        for file in file_names:
            records_list = []  # 为每一个记录文件创建一个列表
            if file.endswith('.xlsx') or file.endswith('.xls'):
                # 读取数据
                file_path = os.path.join(self.input_path, file)
                wb = app.books.open(file_path)  # 打开待转化的工作簿
                sheet = wb.sheets[0]  # 标签页
                for i1, i2 in zip(df_ref["单元格位置"], df_ref["数据操作"]):
                    try:
                        cell_value = sheet.range(i1).value  # 单元格原始值
                        # print(cell_value)
                    except Exception as e:
                        cell_value = "未找到单元格"
                        print("获取表格单元格数据失败：", str(e))
                    value_filted = self.string_manuf(cell_value, i2)  # 调用对应的方法处理原始数据
                    records_list.append(value_filted)  # 提取的数据添加到列表
                    continue
                all_records_list.append(records_list)  # 添加到总列表
                wb.close()  # 关闭工作簿
        app.quit()  # 关闭app
        return all_records_list

    # 写入数据
    def write_data(self, data):
        df = pd.read_excel(self.output_path)
        df2write = pd.DataFrame(data, columns=df.columns)
        df2write.to_excel(self.output_path, index=False)

    # 字符串操作
    def string_manuf(self, s, i):
        if i == 1:
            ss = s.split('：')[0]
        elif i == 2:
            ss = s.split('：')[1]
        elif i == 3:
            ss = s.split()[0]
        elif i == 4:
            ss = s.split()[1]
        elif i == 5:
            ss = s.split(',')[0]
        elif i == 6:
            ss = s.split(',')[1]
        else:
            ss = s
        return ss


if __name__ == "__main__":
    test_instance = Record2Table()
    test_instance.input_path = "./测试数据/警戒潮位值信息统计表"
    test_instance.output_path = "./测试数据/警戒潮位值信息统计表_汇总设计.xlsx"
    test_instance.ref_table_path = "./测试数据/对应关系表.xlsx"
    records = test_instance.read_records()
    test_instance.write_data(records)
    print(records)
    print("汇总数据成功")
