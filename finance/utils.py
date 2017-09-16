import numpy as np
import pandas as pd
import yahoo_tools


def get_detailed_pricing(symbol, src, start_date, end_date):
    if src == "qdl":
        res = {}
        raw_data = quandl(symbol, start_date, end_date)
        for ind,col_name in enumerate(rdata["column_names"][1:]):
            res[col_name] = [i[ind+1] for i in raw_data["data"]]
        return pd.DataFrame(data=res,index=pd.DatetimeIndex([i[0] for i in raw_data["data"]]))
    if src == "yhoo":
        return yahoo_tools.historical_data(symbol, start_date, end_date)

def get_pricing(symbol_list, src, start_date, end_date, field):
    
    res = {}

    if src == "qdl":
        if type(symbol_list) == str:
            r = quandl(symbol_list, start_date, end_date, field=field)
            s = pd.Series([i[1] for i in r["data"]],index=pd.DatetimeIndex([i[0] for i in r["data"]]),dtype=float)
            s.name = symbol_list
            return s
        else:    
            for stock in symbol_list:
                r = quandl(stock, start_date, end_date, field=field)
                res[stock] = pd.Series([i[1] for i in r["data"]],index=pd.DatetimeIndex([i[0] for i in r["data"]]))
            return pd.DataFrame(res)
        
    if src == "yhoo":
        ref = {"open":"Open","high":"High","low":"Low","close":"Close","vol":"Volume"}
        if type(symbol_list) == str:
            r = yahoo_tools.historical_data(symbol_list, start_date, end_date)
            s = r[ref[field]]
            s.name = symbol_list
            return s
        else:
            for stock in symbol_list:
                r = yahoo_tools.historical_data(stock, start_date, end_date)
                try:
                    res[stock] = r[ref[field]]
                except(KeyError):
                    print "Could not read data from %s, skipping" % stock
            return pd.DataFrame(res)

        
def quandl(ticker, start_date, end_date, field=None):
    import requests
    
    ref = {"price":8,"ask": 1, "bid":2, "high": 4, "low": 6, "close": 10}
    if field is None:
        col = None
    else:
        col = ref[field]
    
    url = 'https://www.quandl.com/api/v3/datasets/HKEX/' + ticker + '/data.json'
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': 'CqRnybn2soNJPpEGZCy8',
        'column_index': col,
    }
    cache_timeout = 1*60 # in seconds
    try:
        r = requests.get(url,params=params)
    except requests.exceptions.Timeout:
        return 0
    if r.headers['Content-Type'].startswith('text/html'):
        # 404 not found
        return 0
    else:
        return r.json()["dataset_data"]

def local_csv(fname, mode='h'):
    import csv

    res = {}
    index = []
    with open(fname) as csvfile:
        csvread = csv.reader(csvfile)
        header = next(csvread) # first line is header
        for row in csvread:
            index.append(row[0]) # first column is index
            for ind, el in enumerate(header[1:]):
                try:
                    val = float(row[ind + 1])
                except(ValueError):
                    val = row[ind + 1]
                
                if el in res:
                    res[el].append(val)
                else:
                    res[el]=[val]
                    
    try:
        id = pd.DatetimeIndex(index)
    except(pd.tslib.OutOfBoundsDatetime):
        id = index
    df = pd.DataFrame(data=res, index=id)
    df.index.name = header[0]
    return df