import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from coordinate_crawler import CoordinateCrawler
from file_handler import FileHandler
from record2table import Record2Table
from corr_trans import CorrTrans
from pdf2table import PDF2Table
from field_name_translator import Fn_Translator
from pgDatabase import ReadDatabase
from dataQualityInspection import DataQuaINS
import webbrowser

class SystemUI:
    def __init__(self):
        self.root = tk.Tk()  # tkinter主窗口
        self.root.resizable(0, 0)  # 可调节大小
        self.screen_width = self.root.winfo_screenwidth()  # 获得屏幕宽度
        self.screen_height = self.root.winfo_screenheight()  # 获得屏幕高度

    # 主界面窗口
    def main_UI(self):
        self.root.title("数据批量处理工具")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 4, self.screen_height / 4))
        # 设置窗口背景颜色
        self.root.config(background="#FFFFFF")
        # 设置窗口的透明度
        self.root.attributes('-alpha', 0.9)
        # 添加文本内容,并对字体添加相应的格式 font(字体,字号,"字体类型")
        text1 = tk.Label(self.root, text="数据批量处理工具\n\n--*** ***--", bg="white", fg="red",
                        font=('Times', 25, 'bold'))
        text2 = tk.Label(self.root, text="***-****", bg="white", fg="red",
                         font=('微软雅黑', 10, 'italic'))
        # 将文本内容放置在主窗口内
        text1.pack(expand=True)
        text2.pack(expand=True)
        '''
        # 添加按钮
        button1 = tk.Button(self.root, text="高德地图POI采集", command=self.POI_UI, font=("等线", 20, "bold"), bd=5)
        button2 = tk.Button(self.root, text="坐标转换工具", command=self.corr_trans_UI, font=("等线", 20, "bold"), bd=5)
        button3 = tk.Button(self.root, text="批量提取和汇总", command=self.r2t_UI, font=("等线", 20, "bold"), bd=5)
        button4 = tk.Button(self.root, text="批量提取PDF表格", command=self.pdf_table_UI, font=("等线", 20, "bold"), bd=5)
        button5 = tk.Button(self.root, text="批量翻译字段名称", command=self.translator_UI, font=("等线", 20, "bold"), bd=5)
        # 放置按钮
        button1.pack(expand=1, fill='both', padx='10px', pady='10px')
        button2.pack(expand=1, fill='both', padx='10px', pady='10px')
        button3.pack(expand=1, fill='both', padx='10px', pady='10px')
        button4.pack(expand=1, fill='both', padx='10px', pady='10px')
        button5.pack(expand=1, fill='both', padx='10px', pady='10px')
        '''
        # 创建菜单栏
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # 创建数据提取菜单
        extra_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="数据提取", menu=extra_menu)

        # 为数据提取菜单添加选项
        extra_menu.add_command(label="采集高德地图坐标", command=self.POI_UI)
        extra_menu.add_command(label="批量提取PDF表格", command=self.pdf_table_UI)
        extra_menu.add_command(label="批量提取数据库表信息", command=self.get_ds_info_UI)

        # 创建数据转换菜单
        trans_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="数据转换", menu=trans_menu)

        # 为数据转换菜单添加选项
        trans_menu.add_command(label="坐标转换工具", command=self.corr_trans_UI)

        # 创建数据匹配菜单
        match_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="数据匹配", menu=match_menu)

        # 为数据匹配菜单添加选项
        match_menu.add_command(label="批量提取和汇总表格", command=self.r2t_UI)
        match_menu.add_command(label="批量翻译字段名称", command=self.translator_UI)

        def about():
            messagebox.showinfo("关于", "本软件是由***********内部开发的数据批量处理工具。\n\n  作者：黄晓锋（数据运营部）")

        def document():
            url = 'https://doc.weixin.qq.com/doc/w3_Aa8ASAb2AB8USlvFEafQ0qKg9fUjp?scode=AAYALweMAA4RbnGD1wAa8ASAb2AB8&version=4.1.16.6007&platform=win'
            webbrowser.open(
                url
            )
        # 创建帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="帮助", menu=help_menu)

        # 添加选项
        help_menu.add_command(label="关于", command=about)
        help_menu.add_command(label="使用文档", command=document)
        # 循环控制
        self.root.mainloop()

    # 高德POI采集窗口
    def POI_UI(self):
        self.root = tk.Tk()
        self.root.title("高德地图POI采集")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 4, self.screen_height / 2))
        # 添加控件
        label1 = tk.Label(self.root, text="输入表格：")
        label2 = tk.Label(self.root, text="Key：")
        label1.grid(row=0, sticky="w")
        label2.grid(row=1, sticky="w")
        entry1 = tk.Entry(self.root)
        entry2 = tk.Entry(self.root)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)

        label3 = tk.Label(self.root, text="所在城市列名：")
        label4 = tk.Label(self.root, text="单位地址列名：")
        label3.grid(row=2, sticky="w", pady='5px')
        label4.grid(row=3, sticky="w", pady='5px')

        # 选择输入文件的回调函数
        def input_file():
            # 从本地选择一个文件，并返回文件的目录
            filename = filedialog.askopenfilename()
            if filename != '':
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, filename)  # 设置新文本

            else:
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, '您没有选择任何文件')  # 设置新文本

        # 使用grid()函数来布局，并控制按钮的显示位置
        button1 = tk.Button(self.root, text="选择", width=10, command=input_file)
        button1.grid(row=0, column=2)

        # 创建下拉菜单
        cbox1 = ttk.Combobox(self.root)
        cbox2 = ttk.Combobox(self.root)

        # 使用 grid() 来控制控件的位置
        cbox1.grid(row=2, column=1, pady='5px')
        cbox2.grid(row=3, column=1, pady='5px')

        # 获取列名按钮的回调函数
        def get_col_names():
            file = FileHandler()
            file.input_file_path = entry1.get()
            col_names = file.get_column_names()
            cbox1["value"] = col_names
            cbox2["value"] = col_names

        button3 = tk.Button(self.root, text="获取列名", width=10, command=get_col_names)
        button3.grid(row=2, rowspan=2, column=2)

        content_box = tk.Text(self.root, width=40, height=40)
        content_box.grid(row=5, column=0, columnspan=3, pady=5)

        # 开始采集poi按钮的回调函数
        def get_pois():
            city_col_name = cbox1.get()
            address_col_name = cbox2.get()
            content_box.insert(tk.INSERT, '开始采集高德地图POI...\n')
            corrs_list = []
            file = FileHandler()
            file.input_file_path = entry1.get()
            file.output_file_path = entry1.get() + "_output.xlsx"
            table = file.read_table()
            crawler = CoordinateCrawler()
            key = entry2.get()
            if key != '':
                crawler.key = entry2.get()
            for index, row in table.iterrows():
                crawler.city = row[city_col_name]
                crawler.address = row[address_col_name]
                corr = crawler.crawler()
                corrs_list.append(corr)

                content_box.insert(tk.END, str(corr) + '\n')
                self.root.update()

            table['高德坐标'] = corrs_list
            table_output = table.copy()
            file.output_df = table_output
            file.write_table()
            messagebox.showinfo("提示", "POI采集完毕")

        button4 = tk.Button(self.root, text="开始采集POI", width=10, command=get_pois)
        button4.grid(row=4, column=0, pady=5)

        # 开启事件主循环
        self.root.mainloop()

    # 表格数据批量汇总界面
    def r2t_UI(self):
        self.root = tk.Tk()
        self.root.title("表格数据批量汇总")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 4, self.screen_height / 2))
        # 添加控件
        label1 = tk.Label(self.root, text="表格文件夹：")
        label2 = tk.Label(self.root, text="对应关系表：")
        label3 = tk.Label(self.root, text="输出文件：")
        label1.grid(row=0, sticky="w", pady=10)
        label2.grid(row=1, sticky="w", pady=10)
        label3.grid(row=2, sticky="w", pady=10)
        entry1 = tk.Entry(self.root, width=30)
        entry2 = tk.Entry(self.root, width=30)
        entry3 = tk.Entry(self.root, width=30)
        entry1.grid(row=0, column=1, pady=10)
        entry2.grid(row=1, column=1, pady=10)
        entry3.grid(row=2, column=1, pady=10)

        # 选择输入文件夹的回调函数
        def input_folder():
            # 从本地选择一个文件，并返回文件的目录
            folder = filedialog.askdirectory()
            if folder != '':
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, folder)  # 设置新文本

            else:
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, '您没有选择任何文件')  # 设置新文本

        # 选择对应关系表的回调函数
        def select_ref_table():
            # 从本地选择一个文件，并返回文件的目录
            filename = filedialog.askopenfilename()
            if filename != '':
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, filename)  # 设置新文本
            else:
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, '您没有选择任何文件')  # 设置新文本

        # 选择输出文件的回调函数
        def output_file():
            # 从本地选择一个文件，并返回文件的目录
            filename = filedialog.askopenfilename()
            if filename != '':
                entry3.delete(0, tk.END)  # 清空文本框
                entry3.insert(0, filename)  # 设置新文本
            else:
                entry3.delete(0, tk.END)  # 清空文本框
                entry3.insert(0, '您没有选择任何文件')  # 设置新文本

        # 转化按钮回调函数
        def trans_tab():
            transor = Record2Table()
            transor.input_path = entry1.get()
            transor.ref_table_path = entry2.get()
            transor.output_path = entry3.get()
            try:
                records = transor.read_records()
                transor.write_data(records)
                messagebox.showinfo(title="提示", message="表格转换成功")
            except Exception as e:
                messagebox.showerror(title="错误", message="表格转换失败\n" + str(e))

        # 使用grid()函数来布局，并控制按钮的显示位置
        button1 = tk.Button(self.root, text="选择", width=10, command=input_folder)
        button2 = tk.Button(self.root, text="选择", width=10, command=select_ref_table)
        button3 = tk.Button(self.root, text="选择", width=10, command=output_file)
        button4 = tk.Button(self.root, text="开始转化", width=15, height=3, bg='green', bd=5, font=("黑体", 15),
                            command=trans_tab)
        button1.grid(row=0, column=2, pady=10)
        button2.grid(row=1, column=2, pady=10)
        button3.grid(row=2, column=2, pady=10)
        button4.grid(row=3, column=0, columnspan=3, pady=10)

        # 开启事件主循环
        self.root.mainloop()

    # 坐标转换工具界面
    def corr_trans_UI(self):
        self.root = tk.Tk()
        self.root.title("坐标转换工具")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 4, self.screen_height / 2))
        # 添加控件
        label1 = tk.Label(self.root, text="输入表格路径：")
        label2 = tk.Label(self.root, text="输出表格路径：")
        label3 = tk.Label(self.root, text="转换方法：")

        label1.grid(row=0, sticky="w", pady=10)
        label2.grid(row=1, sticky="w", pady=10)
        label3.grid(row=2, sticky="w", pady=10)

        entry1 = tk.Entry(self.root, width=30)
        entry2 = tk.Entry(self.root, width=30)
        # 创建下拉菜单
        cbox1 = ttk.Combobox(self.root)
        cbox1['value'] = ["火星坐标转WGS84", "WGS84转火星坐标", "火星坐标转百度坐标", "百度坐标转火星坐标", "百度坐标转WGS84", "WGS84转百度坐标"]

        entry1.grid(row=0, column=1, pady=10)
        entry2.grid(row=1, column=1, pady=10)
        cbox1.grid(row=2, column=1, pady=10)

        # 选择输入文件夹的回调函数
        def input_file():
            # 从本地选择一个文件，并返回文件的目录
            path = filedialog.askopenfilename()
            if path != '':
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, path)  # 设置新文本

            else:
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, '您没有选择任何文件')  # 设置新文本

        # 选择输出文件的回调函数
        def output_file():
            # 从本地选择一个文件，并返回文件的目录
            filename = filedialog.asksaveasfilename()
            if filename != '':
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, filename)  # 设置新文本
            else:
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, '您没有选择任何文件')  # 设置新文本

        # 转化按钮回调函数
        def transform():
            trans_way = cbox1.get()

            transor = CorrTrans()
            file_handle = FileHandler()
            file_handle.input_file_path = entry1.get()
            file_handle.output_file_path = entry2.get()
            table = file_handle.read_table()
            wgs_lon_list = []
            wgs_lat_list = []
            try:
                for lon, lat in zip(table['X'], table['Y']):
                    if trans_way == "火星坐标转WGS84":
                        wgs_lon, wgs_lat = transor.gcj02towgs84(lon, lat)
                    elif trans_way == "WGS84转火星坐标":
                        wgs_lon, wgs_lat = transor.wgs84togcj02(lon, lat)
                    elif trans_way == "火星坐标转百度坐标":
                        wgs_lon, wgs_lat = transor.gcj02_bd09(lon, lat)
                    elif trans_way == "百度坐标转火星坐标":
                        wgs_lon, wgs_lat = transor.bd09_gcj02(lon, lat)
                    elif trans_way == "百度坐标转WGS84":
                        wgs_lon, wgs_lat = transor.bd09_wgs84(lon, lat)
                    elif trans_way == "WGS84转百度坐标":
                        wgs_lon, wgs_lat = transor.wgs84_bd09(lon, lat)
                    wgs_lon_list.append(wgs_lon)
                    wgs_lat_list.append(wgs_lat)

                table['trans_lon'] = wgs_lon_list
                table['trans_lat'] = wgs_lat_list
                file_handle.output_df = table.copy()
                file_handle.write_table()
                messagebox.showinfo(title="提示", message="坐标转换完成")
            except Exception as e:
                messagebox.showerror(title="错误", message="坐标转换失败\n" + str(e))

        # 使用grid()函数来布局，并控制按钮的显示位置
        button1 = tk.Button(self.root, text="选择", width=10, command=input_file)
        button2 = tk.Button(self.root, text="选择", width=10, command=output_file)

        button3 = tk.Button(self.root, text="开始转换", width=15, height=3, bg='green', bd=5, font=("黑体", 15),
                            command=transform)
        button1.grid(row=0, column=2, pady=10)
        button2.grid(row=1, column=2, pady=10)

        button3.grid(row=3, column=0, columnspan=3, pady=10)

        lab_text = tk.Label(self.root, text="转换坐标前，请把输入表格的\n经度字段名改为X，纬度字段名改为Y", fg='#7CCD7C',
                            font=('微软雅黑', 15, 'italic'), justify='left')
        lab_text.grid(row=4, column=0, columnspan=3, pady=10)

        # 开启事件主循环
        self.root.mainloop()

    # 提取pdf表格工具界面
    def pdf_table_UI(self):
        self.root = tk.Tk()
        self.root.title("提取PDF文件中的表格")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 3, self.screen_height * 0.6))
        # 添加控件
        label1 = tk.Label(self.root, text="输入文件路径：")
        label2 = tk.Label(self.root, text="输出文件/文件夹路径：")
        label3 = tk.Label(self.root, text="提取方法：")
        label4 = tk.Label(self.root, text="输入PDF页码：")
        label5 = tk.Label(self.root, text="表格与表头偏移距离：")
        label6 = tk.Label(self.root, text="表格所在页面高度1：")
        label7 = tk.Label(self.root, text="表格所在页面高度2：")
        label8 = tk.Label(self.root, text="输入自定义参数：")

        label1.grid(row=0, sticky="w", pady=10)
        label2.grid(row=1, sticky="w", pady=10)
        label3.grid(row=2, sticky="w", pady=10)
        label4.grid(row=3, sticky="w", pady=10)
        label5.grid(row=4, sticky="w", pady=10)
        label6.grid(row=5, sticky="w", pady=10)
        label7.grid(row=6, sticky="w", pady=10)
        label8.grid(row=7, sticky="w", pady=10)

        entry1 = tk.Entry(self.root, width=30)
        entry2 = tk.Entry(self.root, width=30)
        # 创建下拉菜单
        cbox1 = ttk.Combobox(self.root)
        cbox1['value'] = ["提取单个页面的表格", "提取全部表格到一个Excel", "提取全部表格多个Excel", "自定义"]

        entry3 = tk.Entry(self.root, width=10)
        entry4 = tk.Entry(self.root, width=10)
        entry5 = tk.Entry(self.root, width=10)
        entry6 = tk.Entry(self.root, width=10)
        text_box = tk.Text(self.root, width=30, height=5)
        text_box.insert(tk.INSERT, '{"vertical_strategy": "text", "horizontal_strategy": "text","text_x_tolerance": 5,"text_y_tolerance": 5}')

        entry1.grid(row=0, column=1, pady=10)
        entry2.grid(row=1, column=1, pady=10)
        cbox1.grid(row=2, column=1, pady=10)
        entry3.grid(row=3, column=1, pady=10)
        entry4.grid(row=4, column=1, pady=10)
        entry5.grid(row=5, column=1, pady=10)
        entry6.grid(row=6, column=1, pady=10)
        text_box.grid(row=7, column=1, pady=10)

        # 选择输入文件夹的回调函数
        def input_file():
            # 从本地选择一个文件，并返回文件的目录
            path = filedialog.askopenfilename()
            if path != '':
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, path)  # 设置新文本

            else:
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, '您没有选择任何文件')  # 设置新文本

        # 选择输出文件夹的回调函数
        def output_folder():
            # 从本地选择一个文件，并返回文件的目录
            folder = filedialog.askdirectory()
            if folder != '':
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, folder)  # 设置新文本
            else:
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, '您没有选择任何文件')  # 设置新文本

        # 提取按钮回调函数
        def extra():
            method = cbox1.get()

            extractor = PDF2Table()
            extractor.input_file_path = entry1.get()
            extractor.output_file_path = entry2.get()
            if entry3.get() != '':
                extractor.page_num = int(entry3.get()) - 1
            if entry4.get() != '':
                extractor.height_offset = float(entry4.get())
            if method == "提取单个页面的表格":
                try:
                    extractor.extract_table()
                    messagebox.showinfo(title="提示", message="提取表格成功")
                except Exception as e:
                    messagebox.showerror(title="错误", message="提取表格失败\n" + str(e))
            elif method == "提取全部表格到一个Excel":
                try:
                    extractor.extract_all_tables()
                    messagebox.showinfo(title="提示", message="提取表格成功")
                except Exception as e:
                    messagebox.showerror(title="错误", message="提取表格失败\n" + str(e))
            elif method == "提取全部表格多个Excel":
                try:
                    extractor.extract_all_tables2()
                    messagebox.showinfo(title="提示", message="提取表格成功")
                except Exception as e:
                    messagebox.showerror(title="错误", message="提取表格失败\n" + str(e))
            elif method == "自定义":
                a = float(entry5.get())
                b = float(entry6.get())
                dic = text_box.get(tk.INSERT, tk.END)
                try:
                    extractor.extra_table_custom(a, b, dic)
                    messagebox.showinfo(title="提示", message="提取表格成功")
                except Exception as e:
                    messagebox.showerror(title="错误", message="提取表格失败\n" + str(e))

        # 使用grid()函数来布局，并控制按钮的显示位置
        button1 = tk.Button(self.root, text="选择pdf", width=10, command=input_file)
        button2 = tk.Button(self.root, text="选择保存文件夹路径", width=20, command=output_folder)

        button3 = tk.Button(self.root, text="开始提取", width=15, height=3, bg='green', bd=5, font=("黑体", 15),
                            command=extra)
        button1.grid(row=0, column=2, pady=10)
        button2.grid(row=1, column=2, pady=10)

        button3.grid(row=8, column=0, columnspan=3, pady=10)

        # 开启事件主循环
        self.root.mainloop()

    # 批量提取数据库表信息界面
    def get_ds_info_UI(self):
        self.root = tk.Tk()
        self.root.title("批量提取pg库表信息")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 3, self.screen_height * 0.6))
        # 添加控件
        label1 = tk.Label(self.root, text="输入文件路径：")
        label2 = tk.Label(self.root, text="输出文件/文件夹路径：")
        label3 = tk.Label(self.root, text="数据库连接信息：")
        label4 = tk.Label(self.root, text="host:")
        label5 = tk.Label(self.root, text="database:")
        label6 = tk.Label(self.root, text="user:")
        label7 = tk.Label(self.root, text="password:")
        label8 = tk.Label(self.root, text="post:")

        label1.grid(row=0, sticky="w", pady=10)
        label2.grid(row=1, sticky="w", pady=10)
        label3.grid(row=2, sticky="w", pady=10)
        label4.grid(row=3, sticky="w", pady=10)
        label5.grid(row=4, sticky="w", pady=10)
        label6.grid(row=5, sticky="w", pady=10)
        label7.grid(row=6, sticky="w", pady=10)
        label8.grid(row=7, sticky="w", pady=10)

        entry1 = tk.Entry(self.root, width=30)
        entry2 = tk.Entry(self.root, width=30)
        # 创建下拉菜单
        cbox1 = ttk.Combobox(self.root)
        cbox1['value'] = ["获取数据库表名", "获取数据库表元数据-输出word", "获取数据库表元数据-输出excel", "获取数据库表行数和大小", "数据质检"]

        entry3 = tk.Entry(self.root, width=15)
        entry3.insert(0, "19.16.18.135")
        entry4 = tk.Entry(self.root, width=15)
        entry4.insert(0, "db_ocean_dwt")
        entry5 = tk.Entry(self.root, width=15)
        entry5.insert(0, "hyzx_admin")
        entry6 = tk.Entry(self.root, width=15)
        entry6.insert(0, "Admin@2024!")
        entry7 = tk.Entry(self.root, width=15)
        entry7.insert(0, "30001")

        entry1.grid(row=0, column=1, pady=10)
        entry2.grid(row=1, column=1, pady=10)
        entry3.grid(row=3, column=1, pady=10)
        entry4.grid(row=4, column=1, pady=10)
        entry5.grid(row=5, column=1, pady=10)
        entry6.grid(row=6, column=1, pady=10)
        entry7.grid(row=7, column=1, pady=10)
        cbox1.grid(row=8, column=1, pady=10)

        # 选择输入文件夹的回调函数
        def input_file():
            # 从本地选择一个文件，并返回文件的目录
            path = filedialog.askopenfilename()
            if path != '':
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, path)  # 设置新文本

            else:
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, '您没有选择任何文件')  # 设置新文本

        # 选择输出文件夹的回调函数
        def output_folder():
            # 从本地选择一个文件，并返回文件的目录
            folder = filedialog.askdirectory()
            if folder != '':
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, folder)  # 设置新文本
            else:
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, '您没有选择任何文件')  # 设置新文本

        # 提取按钮的回调函数
        def start_extra():
            input_path = entry1.get()
            out_path = entry2.get()
            host = entry3.get()
            database = entry4.get()
            user = entry5.get()
            password = entry6.get()
            port = entry7.get()
            selection = cbox1.get()

            ds_reader = ReadDatabase()
            data_inspector = DataQuaINS()
            ds_reader.input_file_path = input_path
            ds_reader.out_file_path = out_path
            ds_reader.host = host
            ds_reader.database = database
            ds_reader.user = user
            ds_reader.password = password
            ds_reader.port = port

            data_inspector.input_file_path = input_path
            data_inspector.out_file_path = out_path
            data_inspector.host = host
            data_inspector.database = database
            data_inspector.user = user
            data_inspector.password = password
            data_inspector.port = port

            if selection == "获取数据库表名":
                try:
                    ds_reader.get_ds_table_names()
                    messagebox.showinfo("提示", "获取数据库表名成功")
                except Exception as e:
                    messagebox.showerror("错误", str(e))
            elif selection == "获取数据库表元数据-输出word":
                try:
                    ds_reader.get_tables_meta_data()
                    messagebox.showinfo("提示", "获取数据库表元数据成功")
                except Exception as e:
                    messagebox.showerror("错误", str(e))
            elif selection == "获取数据库表元数据-输出excel":
                try:
                    ds_reader.get_tables_meta_data_excel()
                    messagebox.showinfo("提示", "获取数据库表元数据成功")
                except Exception as e:
                    messagebox.showerror("错误", str(e))
            elif selection == "获取数据库表行数和大小":
                try:
                    ds_reader.get_tables_size()
                    messagebox.showinfo("提示", "获取数据库表行数和大小成功")
                except Exception as e:
                    messagebox.showerror("错误", str(e))
            elif selection == "数据质检":
                try:
                    data_inspector.data_qual_insp()
                    messagebox.showinfo("提示", "数据质检完成")
                except Exception as e:
                    messagebox.showerror("错误", str(e))



        # 使用grid()函数来布局，并控制按钮的显示位置
        button1 = tk.Button(self.root, text="选择输入文件", width=10, command=input_file)
        button2 = tk.Button(self.root, text="选择保存文件夹路径", width=20, command=output_folder)

        button3 = tk.Button(self.root, text="开始提取", width=15, height=3, bg='green', bd=5, font=("黑体", 15),
                            command=start_extra)
        button1.grid(row=0, column=2, pady=10)
        button2.grid(row=1, column=2, pady=10)

        button3.grid(row=9, column=0, columnspan=3, pady=10)

        # 开启事件主循环
        self.root.mainloop()

    # 批量翻译字段名称界面
    def translator_UI(self):
        self.root = tk.Tk()
        self.root.title("批量翻译字段名称")
        # 设置窗口大小
        self.root.geometry("%dx%d" % (self.screen_width / 4, self.screen_height / 2))
        # 添加控件
        label1 = tk.Label(self.root, text="字段名称列表：")
        label2 = tk.Label(self.root, text="输出表格：")
        label1.grid(row=0, sticky="w")
        label2.grid(row=1, sticky="w")
        entry1 = tk.Entry(self.root)
        entry2 = tk.Entry(self.root)
        entry1.grid(row=0, column=1)
        entry2.grid(row=1, column=1)

        label3 = tk.Label(self.root, text="appid：")
        label4 = tk.Label(self.root, text="appkey：")
        label3.grid(row=2, sticky="w", pady='5px')
        label4.grid(row=3, sticky="w", pady='5px')
        entry3 = tk.Entry(self.root)
        entry4 = tk.Entry(self.root)
        entry3.grid(row=2, column=1)
        entry4.grid(row=3, column=1)

        # 选择输入文件的回调函数
        def choose_file():
            # 从本地选择一个文件，并返回文件的目录
            filename = filedialog.askopenfilename()
            if filename != '':
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, filename)  # 设置新文本

            else:
                entry1.delete(0, tk.END)  # 清空文本框
                entry1.insert(0, '您没有选择任何文件')  # 设置新文本

        # 选择输出文件的回调函数
        def choose_file1():
            # 从本地选择一个文件，并返回文件的目录
            filename = filedialog.askopenfilename()
            if filename != '':
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, filename)  # 设置新文本

            else:
                entry2.delete(0, tk.END)  # 清空文本框
                entry2.insert(0, '您没有选择任何文件')  # 设置新文本

        # 使用grid()函数来布局，并控制按钮的显示位置
        button1 = tk.Button(self.root, text="选择", width=10, command=choose_file)
        button1.grid(row=0, column=2)
        button2 = tk.Button(self.root, text="选择", width=10, command=choose_file1)
        button2.grid(row=1, column=2)

        content_box = tk.Text(self.root, width=40, height=20)
        content_box.grid(row=5, column=0, columnspan=3, pady=5)

        # 开始采集poi按钮的回调函数
        def trans_words():
            translator = Fn_Translator()
            translator.input_path = entry1.get()
            translator.output_path = entry2.get()
            id = entry3.get()
            key = entry4.get()
            if id != '' and key != '':
                translator.appid = id
                translator.appkey = key
            content_box.insert(tk.INSERT, '开始翻译字段名称...\n')
            self.root.update()
            translator.translator()
            content_box.insert(tk.END, '字段名称翻译完成\n')
            content_box.insert(tk.END, f'翻译结果保存在: {translator.output_path}\n')

        button4 = tk.Button(self.root, text="开始翻译字段", width=10, command=trans_words)
        button4.grid(row=4, column=0, pady=5)

        # 开启事件主循环
        self.root.mainloop()


if __name__ == "__main__":
    system = SystemUI()
    system.main_UI()
