# -*- coding: utf8 -*-
import arcpy
import re

# 设置工作空间和图层
arcpy.env.workspace = r"D:\Documents\工作\数据\地环站点坐标转换.gdb"
table_name = "湛江东海岛海洋环境现状调查站位表"

arcpy.AddField_management(in_table=table_name, field_name="latitude", field_type="DOUBLE", field_alias="纬度")
arcpy.AddField_management(in_table=table_name, field_name="longitude", field_type="DOUBLE", field_alias="经度")
# 修改属性表
# ["LATITUDE", "LONGITUDE"]替换为属性表中经纬度对应的字段名
with arcpy.da.UpdateCursor(table_name, ["纬度", "经度", "latitude", "longitude"]) as cursor:
    for row in cursor:
        # 解析度分秒格式，并转换为十进制度数
        latitude = row[0]
        longitude = row[1]
        
        # 使用正则表达式匹配度分秒数字
        try:
            lat_match = re.match(r'(\d+)[^0-9]*(\d+)[^0-9]*([\d.]+)[^0-9]*', latitude)
            lon_match = re.match(r'(\d+)[^0-9]*(\d+)[^0-9]*([\d.]+)[^0-9]*', longitude)
            #print(lat_match.groups(), lon_match.groups())

            if lat_match and lon_match:
                # 字符串转浮点数
                lat_deg, lat_min, lat_sec = map(float, lat_match.groups())
                lon_deg, lon_min, lon_sec = map(float, lon_match.groups())

                # 转换为十进制度数
                lat_decimal = lat_deg + lat_min / 60.0 + lat_sec / 3600
                lon_decimal = lon_deg + lon_min / 60.0 + lon_sec / 3600
                #print(lat_decimal,lon_decimal)

                # 更新数值
                row[2] = round(lat_decimal, 6)
                row[3] = round(lon_decimal, 6)
                cursor.updateRow(row)
        except:
            continue

# 保存修改
#arcpy.SaveToLayerFile_management(layer, layer_name)
