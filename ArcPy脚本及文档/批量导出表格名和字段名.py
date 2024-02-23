# -*- coding: utf-8 -*-
import arcpy
import csv

# 设置工作空间
arcpy.env.workspace = r"D:\Documents\工作\数据\湛江市典型海洋生态系统基本情况调查与评价报告补充表格.gdb"
# 保存结果的csv文件路径
csv_path1 = r"D:\Documents\工作\数据\地环总站补充表格字段.csv"
csv_path2 = r"D:\Documents\工作\数据\地环总站补充表格名称.csv"
csv_path1 = unicode(csv_path1, 'utf-8')
csv_path2 = unicode(csv_path2, 'utf-8')

"""
# 获取字段名和字段别名
with open(csv_path1, 'wb') as csvfile:
    csv_writer = csv.writer(csvfile)
    #csv_writer.writerow(["field_name", "alias_name"])
    # 如果为要素类数据，使用下面的代码获取字段名和字段别名
    
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        fields = arcpy.ListFields(fc)
        for field in fields:
            csv_writer.writerow([field.name, field.aliasName])
            print(field.name, field.aliasName)
            
    # 如果为表格文件，使用下面的代码获取字段名和字段别名
    
    tbs = arcpy.ListTables()
    for tb in tbs:
        fields = arcpy.ListFields(tb)
        for field in fields:
            fn = field.aliasName.encode('gbk')
            csv_writer.writerow([fn])
            print(field.aliasName)
    

"""
# 获取表名和别名
with open(csv_path2, 'wb') as csvfile:
    csv_writer = csv.writer(csvfile)
    #csv_writer.writerow(["table_name", "alias_name"])
    # 如果为要素类数据，使用下面的代码获取表名和别名
    """
    fcs = arcpy.ListFeatureClasses()
    for fc in fcs:
        # 获取要素类的名称
        fc_name = arcpy.Describe(fc).name

        # 获取要素类的别名
        fc_alias = arcpy.Describe(fc).aliasName
        csv_writer.writerow([fc_name, fc_alias])
        print(fc_name, fc_alias)
            
    # 如果为表格文件，使用下面的代码获取表名和别名
    """
    tbs = arcpy.ListTables()
    for tb in tbs:
        # 获取要素类的名称
        fc_name = arcpy.Describe(tb).name.encode('gbk')
        
        # 获取要素类的别名
        #fc_alias = arcpy.Describe(tb).aliasName
        csv_writer.writerow([fc_name])
        print(fc_name)

