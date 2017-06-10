# encoding = 'utf-8'
import requests
from bs4 import BeautifulSoup
import time
import random
import os
import pandas as pd
import re
import time
import pickle
import traceback
import sqlite3
import os
from functools import *
from datetime import datetime
import dateutil
import numpy as np

def randHeader():
    '''
    随机生成User-Agent
    :return:
    '''
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/ 5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'
                       ]
    result = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return result

def getCurrentTime():
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

def getURL(url, header='rand', tries_num=5, sleep_time=0, time_out=10,max_retry = 5, isproxy=False):
        '''
           这里重写get函数，主要是为了实现网络中断后自动重连，同时为了兼容各种网站不同的反爬策略及，通过sleep时间和timeout动态调整来测试合适的网络连接参数；
           通过isproxy 来控制是否使用代理，以支持一些在内网办公的同学
        :param url:
        :param tries_num:  重试次数
        :param sleep_time: 休眠时间
        :param time_out: 连接超时参数
        :param max_retry: 最大重试次数，仅仅是为了递归使用
        :return: response
        '''
        sleep_time_p = sleep_time
        time_out_p = time_out
        tries_num_p = tries_num
        if header == 'rand':
            header = randHeader()
        
        try:
            res = requests.Session()
            if isproxy == 1:
                res = requests.get(url, headers=header, timeout=time_out, proxies=proxy)
            else:
                res = requests.get(url, headers=header, timeout=time_out)
            res.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            sleep_time_p = sleep_time_p + 10
            time_out_p = time_out_p + 10
            tries_num_p = tries_num_p - 1
            # 设置重试次数，最大timeout 时间和 最长休眠时间
            if tries_num_p > 0:
                time.sleep(sleep_time_p)
                print (getCurrentTime(), url, 'URL Connection Error: 第', max_retry - tries_num_p, u'次 Retry Connection', e)
                return getURL(url, tries_num_p, sleep_time_p, time_out_p,max_retry)
        return res

if __name__ == '__main__':
    refetch_urls = True
    site = 'http://www.chinafund.cn'
    
    # Fetch url list
    if refetch_urls:
        urls = []
        for i in range(1,21):
            print('Fetching page %d...' % i)
            try:
                res = getURL('http://www.chinafund.cn/tree/sjzx/kjrjz_%d.html' % i)
                res.encoding='gbk'
                soup = BeautifulSoup(res.text,'html.parser')
                urls += [(a.attrs['title'],a.attrs['href']) for a in soup.select('ul.pagelist li a')]
            except:
                print("ERROR in fetching page %d!" % i)
            time.sleep(1)

        pickle.dump(urls,open('./data/urls','wb'))
    else:
        urls = pickle.load(open('./data/urls','rb'))
        
    # Crawl data from site
    err_cnt = 0
    for url in urls:
        if os.path.exists('./data/%s.csv' % url[0]):
            print('Using cached result: %s'%url[1])
            continue

        print('Fetching url:%s'%url[1])
        try:
            res = getURL(site + url[1])
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text,'html.parser')
            df = pd.read_html(str(soup.select('table')[0]),header=0)[0]
            df.to_csv('./data/%s.csv'%url[0],index=None,encoding='gb2312')
        except:
            print('Error in fetching url:%s, the title is %s'%(url[1], url[0]))
            traceback.print_exc()
            err_cnt += 1
            if err_cnt > 1:
                time.sleep(300)

        sleep_time = random.gauss(1,0.5)
        if sleep_time < 0.5:
            sleep_time = 0.5
        time.sleep(sleep_time)
        
    # Save data into database
    conn = sqlite3.connect('./data/fund-data.db')
    sql = """
    CREATE TABLE fundValue (
        code int NOT NULL, 
        name varchar(50) NOT NULL, 
        trade_date date NOT NULL, 
        net_val decimal, 
        acc_net decimal, 
        day_growth_percent decimal
    );
    """
    conn.execute(sql)
    sql = "CREATE INDEX idx_fund ON fundValue (code, trade_date);"
    conn.execute(sql)
    fns = list(filter(lambda s:'csv' in s, os.listdir('./data')))

    for fn in fns:
        date = re.findall('\d+-\d+-\d+',fn)[0]
        sql = 'select code from fundValue where trade_date = "%s"' % date
        rst = conn.execute(sql)
        if rst.fetchone() != None:
            print('Date %s is already in the database' % date)
            continue

        print('Reading date %s...' % date)
        df = pd.read_csv('./data/'+fn,encoding='gb2312',na_values=('--'))

        float_cols = ['最新净值','累计净值','日增长率%']

        for cn in float_cols:
            col = df[cn]
            if col.dtype != np.dtype('float'):
                values = []
                for c in col:
                    try:
                        v = float(c)
                    except:
                        try:
                            v = float(re.findall('[-+]?[0-9]*\.?[0-9]+',c)[0])
                        except:
                            v = np.nan
                    values.append(v)
                df[cn] = values

        for i in range(len(df)):
            row = df.iloc[i]

            if np.isnan(row[2]) or np.isnan(row[3]) or np.isnan(row[4]):
                continue

            sql = """insert into fundValue(code, name, trade_date, net_val, acc_net, day_growth_percent) 
                values('%d', '%s', '%s', '%f', '%f', '%f')""" % \
                (row[0], row[1], date, row[2], row[3], row[4])
            conn.execute(sql)
        conn.commit()
    conn.close()