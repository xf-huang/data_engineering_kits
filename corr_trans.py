#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    ————————————————
    坐标转换代码来自CSDN博主「地学大数据」的原创文章
    原文链接：https: // blog.csdn.net / chenxu0136 / article / details / 119361975
"""
import math

class CorrTrans:
    def __init__(self):
        self.pi = 3.1415926535897932384626  # π
        self.r_pi = self.pi * 3000.0 / 180.0
        self.la = 6378245.0  # 长半轴
        self.ob = 0.00669342162296594323  # 扁率

    # 火星坐标转WGS84坐标
    def gcj02towgs84(self, lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:
        """
        if self.out_of_china(lng, lat):
            return lng, lat
        dlat = self.transformlat(lng - 105.0, lat - 35.0)
        dlng = self.transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ob * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.la * (1 - self.ob)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.la / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    # WGS84坐标转火星坐标
    def wgs84togcj02(self, lon_wgs84, lat_wgs84):
        if self.out_of_china(lon_wgs84, lat_wgs84):  # 判断是否在国内
            return [lon_wgs84, lat_wgs84]
        tlat = self.transformlat(lon_wgs84 - 105.0, lat_wgs84 - 35.0)
        tlng = self.transformlng(lon_wgs84 - 105.0, lat_wgs84 - 35.0)
        rlat = lat_wgs84 / 180.0 * self.pi
        m = math.sin(rlat)
        m = 1 - self.ob * m * m
        sm = math.sqrt(m)
        tlat = (tlat * 180.0) / ((self.la * (1 - self.ob)) / (m * sm) * self.pi)
        tlng = (tlng * 180.0) / (self.la / sm * math.cos(rlat) * self.pi)
        lat_gcj02 = lat_wgs84 + tlat
        lon_gcj02 = lon_wgs84 + tlng
        return [lon_gcj02, lat_gcj02]

    # 火星坐标转百度坐标
    def gcj02_bd09(self, lon_gcj02, lat_gcj02):
        b = math.sqrt(lon_gcj02 * lon_gcj02 + lat_gcj02 * lat_gcj02) + 0.00002 * math.sin(lat_gcj02 * self.r_pi)
        o = math.atan2(lat_gcj02, lon_gcj02) + 0.000003 * math.cos(lon_gcj02 * self.r_pi)
        lon_bd09 = b * math.cos(o) + 0.0065
        lat_bd09 = b * math.sin(o) + 0.006
        return [lon_bd09, lat_bd09]

    # 百度坐标转火星坐标
    def bd09_gcj02(self, lon_bd09, lat_bd09):
        m = lon_bd09 - 0.0065
        n = lat_bd09 - 0.006
        c = math.sqrt(m * m + n * n) - 0.00002 * math.sin(n * self.r_pi)
        o = math.atan2(n, m) - 0.000003 * math.cos(m * self.r_pi)
        lon_gcj02 = c * math.cos(o)
        lat_gcj02 = c * math.sin(o)
        return [lon_gcj02, lat_gcj02]

    # 百度坐标转WGS84坐标
    def bd09_wgs84(self, lon_bd09, lat_bd09):
        # 先把百度坐标系的经纬度转换为火星坐标系
        tmpList_gcj02 = self.bd09_gcj02(lon_bd09, lat_bd09)
        # 然后把火星坐标系的坐标转换为WGS84坐标系
        return self.gcj02towgs84(tmpList_gcj02[0], tmpList_gcj02[1])

    # WGS84转百度坐标
    def wgs84_bd09(self, lon_wgs84, lat_wgs84):
        # 先把wgs84坐标系的坐标转换为火星坐标系
        tmpList_gcj02 = self.wgs84togcj02(lon_wgs84, lat_wgs84)
        # 然后把火星坐标系的坐标转换为百度坐标系
        return self.gcj02_bd09(tmpList_gcj02[0], tmpList_gcj02[1])

    def transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng:
        :param lat:
        :return:
        """
        if lng < 72.004 or lng > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False


if __name__ == '__main__':
    test_instance = CorrTrans()
    wgs_lon, wgs_lat = test_instance.gcj02towgs84(113.198771, 22.098893)
    gcj_lon, gcj_lat = test_instance.wgs84togcj02(wgs_lon, wgs_lat)
    bd_lon, bd_lat = test_instance.gcj02_bd09(wgs_lon, wgs_lat)
    gcj2_lon, gcj2_lat = test_instance.bd09_gcj02(bd_lon, bd_lat)
    wgs2_lon, wgs2_lat = test_instance.bd09_wgs84(bd_lon, bd_lat)
    bd2_lon, bd2_lat = test_instance.wgs84_bd09(wgs_lon, wgs_lat)
    print("火星转WGS", wgs_lon, wgs_lat)
    print("WGS转火星", gcj_lon, gcj_lat)
    print("火星转百度", bd_lon, bd_lat)
    print("百度转火星", gcj2_lon, gcj2_lat)
    print("百度转WGS", wgs2_lon, wgs2_lat)
    print("WGS转百度", bd2_lon, bd2_lat)

