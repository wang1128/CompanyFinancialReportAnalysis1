# -*- coding : utf-8 -*- #

'''最近12个月的财报'''
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

    # 下载三张报表
    def req(self, ninfo):
        # try:
        info = ninfo
        scode = info["SECCODE"]
        # year=info["year"]
        # print(scode,year)
        data_ = info
        url0 = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{}/ctrl/part/displaytype/4.phtml'.format(
            scode)
        url1 = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{}/ctrl/part/displaytype/4.phtml'.format(
            scode)
        url2 = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{}/ctrl/part/displaytype/4.phtml'.format(
            scode)
        url_list = []
        url_list.extend([url0, url1, url2])
        # data_year=[]
        data = {}
        for url in url_list:
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip,deflate,br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
                "upgrade-insecure-requests": "1",
                "user-agent": self.usa.random, }
            response = requests.get(url, headers=headers)  # ,headers=headers
            # print(response.text)
            soup = BeautifulSoup(response.content.decode("GBK"), "lxml")

            '''报表日期'''
            trs = soup.select("tbody tr")

            for tr in trs:
                tds = tr.select("td")
                if tds[1:] != []:
                    # print(tds)
                    # try:
                    value_list = []
                    # value = [td.text for td in tds[1:]]
                    for td in tds[1:]:
                        td = td.text
                        # print(td)

                        if td == "--":
                            td = 0.00

                        try:
                            value_list.append(float(td.replace(',', '')))
                            # data[tds[0].text] =
                        except:
                            value_list.append(td)
                            # data[tds[0].text] = td
                    data[tds[0].text] = value_list
                    # except:
                    #     pass

            # print(data)
            # data_year.append(data)
            data_.update(data)
        # print(data_)
        # data_["data"]=data_year
        print(info["SECNAME"])
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
            try:
                self.req(info)
                self.write_json()
                time.sleep(2)
            except:
                try:
                    time.sleep(5)
                    print("Retry!")
                    self.req(info)
                    self.write_json()
                except:
                    print("************* error *******")
                    pass

        self.write_json()

    def write_json(self):
        try:
            # 建立连接
            client = pymongo.MongoClient('localhost', 27017)
            # 建立数据库
            db = client["XinlangFinance"]

            # 从原有的txt文件导入share_id：

            # 表的对象化
            mgtable = Collection(db, 'FinanceReport_data_n12_final')

            mgtable.insert_many(self.dict_list)
            result = self.dict_list.pop()
            print(result)

        except:
            print("写入出错！！")
            pass


if __name__ == '__main__':
    start_time = time.time()

    X = Xinalang()
    X.scheduler()

    print("总耗时：{}秒".format(time.time() - start_time))
