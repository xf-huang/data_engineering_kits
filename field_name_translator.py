import pandas as pd
import requests
import random
from hashlib import md5
import re
import time


class Fn_Translator:
    def __init__(self):
        # Set your own appid/appkey.
        self.appid = '20231114001880377'
        self.appkey = 'YYbTN1XlJwrTBgiRzO9k'

        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
        self.from_lang = 'zh'
        self.to_lang = 'en'

        self.input_path = r""
        self.output_path = r""

        self.endpoint = 'http://api.fanyi.baidu.com'
        self.path = '/api/trans/vip/translate'
        self.url = self.endpoint + self.path

    def translator(self):
        # 存放翻译结果字典
        field_dist = {"字段名": [],
                      "英文名称": [],
                      "长度": []}
        if self.input_path.endswith(".xlsx") or self.input_path.endswith(".xls"):
            field_df = pd.read_excel(self.input_path, header=None)
        if self.input_path.endswith(".csv"):
            field_df = pd.read_csv(self.input_path, header=None, encoding='ANSI')
        fields_all = field_df.loc[:, 0].to_list()
        for field in fields_all:
            s = field
            # 去除括号中的内容
            query = re.sub('[\(（].*[\)）]', '', s)

            # print(query)

            if query.isascii():
                field_dist["字段名"].append(query)
                field_dist["英文名称"].append(query)
                field_dist["长度"].append(len(query))
            else:
                # Generate salt and sign
                def make_md5(s, encoding='utf-8'):
                    return md5(s.encode(encoding)).hexdigest()
                salt = random.randint(32768, 65536)
                sign = make_md5(self.appid + query + str(salt) + self.appkey)

                # Build request
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                payload = {'appid': self.appid, 'q': query, 'from': self.from_lang, 'to': self.to_lang, 'salt': salt,
                           'sign': sign}

                # Send request
                try:
                    r = requests.post(self.url, params=payload, headers=headers)
                    result = r.json()
                    # print(result)
                    res = result["trans_result"][0]['dst']
                    res_ = '_'.join(res.upper().split())
                    print(field, res_)
                    length = len(res_)
                    field_dist["字段名"].append(s)
                    field_dist["英文名称"].append(res_)
                    field_dist["长度"].append(length)
                    time.sleep(1)
                except:
                    continue

        df = pd.DataFrame(field_dist)
        if self.output_path.endswith(".csv"):
            df.sort_values(by='长度').to_csv(self.output_path, index=False)
        if self.output_path.endswith(".xlsx") or self.output_path.endswith(".xls"):
            df.sort_values(by='长度').to_excel(self.output_path, index=False)
        print("字段名翻译完成")


if __name__ == "__main__":
    trans_test = Fn_Translator()
    trans_test.input_path = r"D:\Documents\工作\数据\地环总站补充表格名称.xlsx"
    trans_test.output_path = r"D:\Documents\工作\数据\地环总站表名和字段名\地环总站补充表格名称翻译.xlsx"
    trans_test.translator()
    print("字段名翻译完成")
