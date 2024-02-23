# -*- coding: utf-8 -*-
import arcpy
# 替换为需要添加字段的gdb文件路径
arcpy.env.workspace = r"C:\Users\admin\Desktop\新建文件夹 (4)\地市合并.gdb"
# 获取gdb中所有要素类
feature_classes = arcpy.ListFeatureClasses()
# 替换为需要添加的字段信息，列表中一个元组为一个字段，元组中第一个元素是字段名，第二个元素是字段类型，第三个元素是字段别名，第四个元素是字段长度
fields_to_add = [
	("OCEAN_DATA_IDENTIFICATION_CODE", "TEXT", "海洋数据标识码", 27),
	("ADMINISTRATIVE_DIVISION", "TEXT", "行政区划", 64),
	("ADMINISTRATIVE_DIVISION_CODE", "TEXT", "行政区划代码", 12),
	("GEO_AREA", "DOUBLE", "几何面积（平方米）", None)
	]
# 循环为gdb中每个要素类添加字段
for fc in feature_classes:
	for field in fields_to_add:
		name, data_type, alias, length = field
		arcpy.AddField_management(in_table=fc, field_name=name, field_type=data_type, field_length=length, field_alias=alias)
print("添加字段成功")
