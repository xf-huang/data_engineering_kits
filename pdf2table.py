import pdfplumber
import pandas as pd
import os
from operator import itemgetter
import json

class PDF2Table:
    def __init__(self):
        self.page_num = 0  # 页码
        self.height_offset = 50  # 高度偏移距离
        self.input_file_path = ""
        self.output_file_path = ""

    # 提取单个页面的表格
    def extract_table(self):
        table_rows_list = []
        table_settings = {
            "horizontal_strategy": "lines",
            "vertical_strategy": "lines"
        }
        with pdfplumber.open(self.input_file_path) as pdf:
            page = pdf.pages[self.page_num]
            tables_found = page.find_tables(table_settings)
            if tables_found:
                for table in tables_found:
                    width_up, height_up, width_low, height_low = table.bbox
                    crop = page.crop((0, height_up, page.width, height_low))
                    edgel = sorted(crop.horizontal_edges, key=itemgetter("x0"))[0]
                    edger = sorted(crop.horizontal_edges, key=itemgetter("x1"))[-1]
                    table_extract = crop.extract_table({"vertical_strategy": "lines", "explicit_vertical_lines": [edgel["x0"], edger["x1"]]})
                    table_head = page.within_bbox((width_up, height_up - self.height_offset, width_low, height_up))
                    table_head = table_head.extract_text().split('\n')[-1]
                    # table_rows_list.append([table_head])
                    for row in table_extract:
                        table_rows_list.append(row)
                    table_rows_list.append([])
        df = pd.DataFrame(table_rows_list)
        df.to_excel(os.path.join(self.output_file_path, f"{table_head}.xlsx"), index=None, header=False)

    # 提取PDF中所有表格到同一个Excel表格中
    def extract_all_tables(self):
        table_rows_list = []
        with pdfplumber.open(self.input_file_path) as pdf:
            pages_count = len(pdf.pages)
            for i in range(pages_count):
                page = pdf.pages[i]
                tables_found = page.find_tables()
                if tables_found:
                    for table in tables_found:
                        width_up, height_up, width_low, height_low = table.bbox
                        crop = page.crop((0, height_up, page.width, height_low))
                        edgel = sorted(crop.horizontal_edges, key=itemgetter("x0"))[0]
                        edger = sorted(crop.horizontal_edges, key=itemgetter("x1"))[-1]
                        table_extract = crop.extract_table(
                            {"vertical_strategy": "lines", "explicit_vertical_lines": [edgel["x0"], edger["x1"]]})
                        table_head = page.within_bbox((width_up, height_up - self.height_offset, width_low, height_up))
                        table_head = table_head.extract_text().split('\n')[-1]
                        table_rows_list.append([table_head])
                        for row in table_extract:
                            table_rows_list.append(row)
                        table_rows_list.append([])
        df = pd.DataFrame(table_rows_list)
        df.to_excel(os.path.join(self.output_file_path, "输出表格.xlsx"), encoding='utf-8', index=None, header=False)

    # 提取PDF中所有表格，每个表格输出到单独excel
    def extract_all_tables2(self):
        with pdfplumber.open(self.input_file_path) as pdf:
            pages_count = len(pdf.pages)
            table_list = []
            table_head_list = []
            k = 0
            for i in range(pages_count):
                page = pdf.pages[i]
                tables_found = page.find_tables()
                if tables_found:
                    for table in tables_found:
                        width_up, height_up, width_low, height_low = table.bbox
                        crop = page.crop((0, height_up, page.width, height_low))
                        edgel = sorted(crop.horizontal_edges, key=itemgetter("x0"))[0]
                        edger = sorted(crop.horizontal_edges, key=itemgetter("x1"))[-1]
                        table_extract = crop.extract_table(
                            {"vertical_strategy": "lines", "explicit_vertical_lines": [edgel["x0"], edger["x1"]]})
                        table_head = page.within_bbox((width_up, height_up - self.height_offset, width_low, height_up))
                        table_head = table_head.extract_text().split('\n')[-1]
                        if table_head.startswith("表") or table_head.startswith("附表") or table_head.startswith("附录"):
                            table_list.append(table_extract)
                            table_head = table_head.replace('/', '_')
                            table_head_list.append(table_head)
                            k += 1
                        else:
                            table_list[k - 1].extend(table_extract)
            save_folder = os.path.join(self.output_file_path, self.input_file_path.split('/')[-1])
            os.makedirs(save_folder, exist_ok=True)

            j = 0
            for table in table_list:
                df = pd.DataFrame(table)
                table_head = table_head_list[j]
                j += 1
                df.to_excel(os.path.join(save_folder, table_head + ".xlsx"), index=None, header=False)

    # 自定义
    def extra_table_custom(self, a, b, dic):
        table_settings = json.loads(dic)
        with pdfplumber.open(self.input_file_path) as pdf:
            page = pdf.pages[self.page_num]
            crop = page.crop((0, page.height * a, page.width, page.height * b))
            table = crop.extract_table(table_settings)
            df = pd.DataFrame(table)
            df.to_excel(os.path.join(self.output_file_path, "输出表格.xlsx"), index=None, header=False)


if __name__ == "__main__":
    test = PDF2Table()
    test.page_num = 73
    test.input_file_path = "./测试数据/3 米锚系浮标海上布放站位考察与站点论证报告.pdf"
    # test.output_file_path = "./输出数据/单个表格输出测试.xlsx"
    # test.output_file_path = "./输出数据/全部表格输出测试.xlsx"
    test.output_file_path = "./输出数据"
    # test.extract_table()
    # test.extract_all_tables()
    dic = '{"vertical_strategy": "text", "horizontal_strategy": "text","text_x_tolerance": 5,"text_y_tolerance": 5}'
    test.extra_table_custom(0, 0.7, dic)
