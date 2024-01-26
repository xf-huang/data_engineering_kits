import requests
import json


class CoordinateCrawler:
    def __init__(self):
        self.key = "5a048ecc2fe5f52d181c8da5a6efb2cf"  # 高德地图key
        self.base_url = "https://restapi.amap.com/v3/geocode/geo?"  # 基础url
        self.address = ""  # 地址
        self.name = ""  # 单位名称
        self.city = ""  # 所属地市

    def crawler(self):
        if self.address != "":
            url = self.base_url + f"key={self.key}&address={self.address}&city={self.city}"  # 完整url
        elif self.name != "":
            url = self.base_url + f"key={self.key}&address={self.name}&city={self.city}"
        else:
            url = ""
        try:
            r = requests.get(url)
            dicts = json.loads(r.text)  # 处理返回的JSON
            code = dicts["geocodes"][0]["location"]  # 提取坐标
        except Exception as e:
            code = ""
            print(f"获取'{self.address}'坐标时出现错误：" + str(e))
        return code


# 单元测试
if __name__ == "__main__":
    test_crawler = CoordinateCrawler()
    test_crawler.city = "广州市"
    test_crawler.address = "广州市海珠区昌岗中路245号"
    test_crawler.name = "广州奈思酒店管理有限公司"
    code = test_crawler.crawler()
    print(code)
    print(test_crawler.address)
