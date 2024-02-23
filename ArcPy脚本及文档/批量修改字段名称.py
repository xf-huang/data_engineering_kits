# -*- coding: utf-8 -*-
import arcpy
import csv

arcpy.env.workspace = r"D:\Documents\工作\数据\湛江市典型海洋生态系统基本情况调查与评价报告补充表格.gdb"
csv_path = r"D:\Documents\工作\数据\地环总站表名和字段名\地环总站补充表格字段翻译.csv"
csv_path = unicode(csv_path, 'utf-8')

# 获取工作空间中的所有表格
tbs = arcpy.ListTables()
# 当工作空间中为要素类数据时，使用下面代码获取表格
# tbs = arcpy.ListFeatureClasses()

# 读取字段翻译，构建字典
field_map = {}
with open(csv_path) as f:
    reader = csv.reader(f)
    for row in reader:
        key = unicode(row[0], 'gbk')
        field_map[key] = row[1]

# 遍历表格，修改字段名称
for tb in tbs:
    fields = arcpy.ListFields(tb)
    for f in fields:
        try:
            key = f.aliasName.encode('utf-8')
            name_change = field_map[key]
            arcpy.management.AlterField(tb, f.name, name_change)
            print("字段重命名成功"+key.encode('utf-8'))
        except:
            print("字段重命名失败"+key.encode('utf-8'))
            continue
    
print("更改字段名完成")


