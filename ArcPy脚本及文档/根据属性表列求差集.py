# -*- coding: utf8 -*-
import arcpy

# 设置工作空间
arcpy.env.workspace = r"D:\Documents\工作\数据\公共用海融合.gdb"


# 第一个矢量数据属性表
first_feature_class = "广东省公共用海点_新增"
# 第二个矢量数据属性表
second_feature_class = "汕尾排污口新增"

# 用集合存储第二个表中 b 列的数据
b_values = set()
with arcpy.da.SearchCursor(first_feature_class, "public_sea_name") as cursor:
    for row in cursor:
        b_values.add(row[0])

# 删除第一个表中匹配第二个表的数据行
with arcpy.da.UpdateCursor(second_feature_class, "public_sea_name") as cursor:
    for row in cursor:
        if row[0] in b_values:
            cursor.deleteRow()

