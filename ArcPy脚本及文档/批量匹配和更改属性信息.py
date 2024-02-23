# -*- coding: utf-8 -*-
import arcpy
import csv

# 设置工作空间
arcpy.env.workspace = r"D:\Documents\工作\数据\广东省2009_2019年风暴潮灾害点.gdb"
csv_path = r"D:\Documents\工作\数据\台风编码.csv"
fc_name = "DWT_GD_2009_2019_STORM_TIDE"

csv_path = unicode(csv_path, 'utf-8')

# 读取台风编码数据并构建字典
tf_code = {}
with open(csv_path) as f:
    reader = csv.reader(f)
    for row in reader:
        name = unicode(row[2], 'gbk')
        tf_code[name] = row[1]

# 匹配台风编号并更新属性值
with arcpy.da.UpdateCursor(fc_name, ["TYPHOON", "TYPHOON_CODE"]) as cursor:
    for row in cursor:
        name = row[0]
        try:
            row[1] = tf_code[name]
            cursor.updateRow(row)
        except:
            continue

print("属性值匹配和更新完成")

