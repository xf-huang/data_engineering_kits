# -*- coding: utf-8 -*-
import arcpy
import csv

# 设置工作空间
arcpy.env.workspace = r"D:\Documents\工作\数据\湛江市典型海洋生态系统基本情况调查与评价报告补充表格.gdb"
csv_path = r"D:\Documents\工作\数据\地环总站表名和字段名\地环总站补充表格名称翻译.csv"
csv_path = unicode(csv_path, 'utf-8')

# 读取表格名称翻译表，构建字典
tb_map = {}
with open(csv_path) as f:
    reader = csv.reader(f)
    for row in reader:
        key = unicode(row[0], 'gbk')
        tb_map[key] = row[1]

# 获取工作空间中的所有表格
table_list = arcpy.ListTables()

# 当工作空间中为要素类数据时，使用下面代码获取表格
# table_list = arcpy.ListFeatureClasses()

# 循环处理每个表格
for table_name in table_list:
    # 新的表格名称，这里可以根据需要修改命名规则
    new_table_name = tb_map[table_name]

    try:
        # 使用Rename_management函数重命名表格
        arcpy.management.Rename(table_name, new_table_name)
        # 使用AlterAliasName函数修改表格别名
        arcpy.AlterAliasName(new_table_name, table_name)
        #print(f"表格 {table_name} 重命名为 {new_table_name}")
    except:
        print("无法重命名表格")
