import akshare as ak

# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907', adjust="")
# print(stock_zh_a_hist_df)


stock_info_a_code_name = ak.stock_info_a_code_name()
print(stock_info_a_code_name)

stock_info_a_code_name.to_csv("stockCode/stock_info_a_code_name", sep='\t', encoding='utf-8')

# 深证证券交易所股票代码和简称
# stock_info_sz_name_code = ak.stock_info_sz_name_code()
# print(stock_info_sz_name_code)
#
# stock_info_sz_name_code.to_csv("stockCode/stock_info_sz_name_code", sep='\t', encoding='utf-8')
#
# # 上海证券交易所股票代码和简称
# stock_info_sh_name_code = ak.stock_info_sh_name_code()
# print(stock_info_sh_name_code)
#
# stock_info_sh_name_code.to_csv("stockCode/stock_info_sh_name_code", sep='\t', encoding='utf-8')

# stock_board_industry_cons_em = ak.stock_board_industry_cons_em()
#
# print(ak.stock_board_industry_name_em())
# stock_board_industry_name_em = ak.stock_board_industry_name_em()
# print(stock_board_industry_name_em['板块名称'])
# for element in stock_board_industry_name_em['板块名称']:
#     print(element)
#     print(ak.stock_board_industry_cons_em(element))
