import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

info=[]
urls = [f'https://search.51job.com/list/020000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,{i}.html' for i in range(1,31)]
for url in urls:
    time.sleep(3)
    web_data = requests.get(url)
    web_data.encoding = 'gbk'
    soup = BeautifulSoup(web_data.text,'lxml')

    positions = soup.select('div > p > span > a')
    companys = soup.select('div > span.t2 > a')
    addresses = soup.select('#resultList > div > span.t3')[1:]
    salaries = soup.select('div > span.t4')[1:]
    publies_times = soup.select('div > span.t5')[1:]

    for position,company,address,salary,publies_time in zip(positions,companys,addresses,salaries,publies_times):
         data = {
             'position':position.get_text().strip(),
             'company':company.get_text(),
             'address':address.get_text(),
             'salary':salary.get_text(),
             'publies_time':publies_time.get_text(),
             'company_link':company.get('href'),
             'position_link':position.get('href'),
         }
         info.append(data)
    print(len(info))

result = pd.DataFrame(info)[['position','company','address','salary','publies_time','company_link','position_link']]

writer = pd.ExcelWriter('/Users/xuelei/Desktop/51job_上海_数据分析01.xlsx')
result.to_excel(writer, 'Sheet1')
writer.save()