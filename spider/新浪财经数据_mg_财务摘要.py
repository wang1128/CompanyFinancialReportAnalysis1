# -*- coding : utf-8 -*- #

'''最近5年的财报财务摘要'''
from multiprocessing import Queue

import pymongo
import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pymongo.collection import Collection


class Xinalang():
    def __init__(self):
        self.queue = Queue()
        self.info = []
        self.dict_list = []
        self.usa = UserAgent()

    # 下载财务简报
    def req(self, ninfo):
        # try:
        info = ninfo
        scode = info["SECCODE"]

        data_ = info
        url0 = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/{}.phtml'.format(scode)
        url_list = []
        url_list.extend([url0])
        # data = {}
        for url in url_list:
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip,deflate,br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "upgrade-insecure-requests": "1",
                "user-agent": self.usa.random, }
            response = requests.get(url, headers=headers, timeout=200)  # ,headers=headers
            # print(response.text)
            html_text = response.content.decode("GBK")
            html1 = html_text.split("FundHoldSharesTable")[1].split("<!--财务摘要end-->")[0]
            html2 = html1.split("<!--分割数据的空行begin-->")
            for h in html2:
                li = {}
                soup = BeautifulSoup(h, "lxml")

                for tr in soup.select("tr"):
                    try:
                        key = tr.select("td")[0].text
                        value = tr.select("td")[1].text
                        if value == "\xa0":
                            value = None
                        elif key == '截止日期':
                            value = value
                        else:
                            value = float(value.replace("元", "").replace(",", ""))

                        li[key] = value
                    except:
                        pass
                if li != {}:
                    data_[li["截止日期"]] = li
                    # print(li)
            '''报表日期'''

        print(info["SECNAME"])
        print(data_)
        self.dict_list.append(data_)

    def scheduler(self):

        with open("stockCode/stock_info_a_code_name", encoding="utf8") as f:
            lines = f.readlines()
        c = -1
        for line in lines[0:]:

            stock_code = line.strip().split("\t")[1]
            stock_name = line.strip().split("\t")[2]

            info = {}
            info["SECCODE"] = stock_code
            info["SECNAME"] = stock_name

            print(info)

            try:
                self.req(info)
            except:
                try:
                    time.sleep(5)
                    print("Retry!")
                    self.req(info)
                except:
                    print("************* error *******")
                    pass
            self.write_json()
            time.sleep(2)

        self.write_json()

    def write_json(self):
        try:
            # 建立连接
            client = pymongo.MongoClient('localhost', 27017)
            # 建立数据库
            db = client["XinlangFinance"]

            # 从原有的txt文件导入share_id：

            # 表的对象化
            mgtable = Collection(db, 'FinanceReport_data_final')

            mgtable.insert_many(self.dict_list)
            result = self.dict_list.pop()
            print("result are :")
            print(result)

        except:
            print("写入出错！！")
            pass


if __name__ == '__main__':
    start_time = time.time()

    X = Xinalang()
    X.scheduler()

    print("总耗时：{}秒".format(time.time() - start_time))
