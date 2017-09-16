import requests
import os
import yaml
import re
import numpy as np
import pandas as pd
import datetime
import time
import io

def get_token():
    # search with regular expressions, "CrumbStore":\{"crumb":"(?<crumb>[^"]+)"\}
    url = 'https://uk.finance.yahoo.com/quote/AAPL/history' # url for a ticker symbol, with a download link
    r = requests.get(url)  # download page
    txt = r.text # extract html
    
    cookie = r.cookies['B'] # the cookie we're looking for is named 'B'
    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

    for line in txt.splitlines():
        m = pattern.match(line)
        if m is not None:
            crumb = m.groupdict()['crumb']
            
    return {"cookie" : cookie, "crumb" : crumb}
    
def save_token(path):
    data = get_token()
    with open(path,'w') as fid:
        yaml.safe_dump(data,fid)
    return data
    
def refresh_token():
    dataDir = "temp/"
    dataFile = dataDir + "yahoo_cookie.yml"
    if not os.path.exists(dataFile):
        if not os.path.exists(dataDir):
            os.mkdir(dataDir)
        # save data to YAML file
        return save_token(dataFile)
    elif time.time() - os.stat(dataFile).st_mtime > 365*24*60*60:
        # token expired
        return save_token(dataFile)
    else:
        with open(dataFile,'r') as fid:
            try:
                token = yaml.safe_load(fid)
            except(yaml.YAMLError):
                print "Cookie could not be read."
                os.remove(dataFile)
                return refresh_token()
            return token
            
def str_to_timestamp(date_str):
    return time.mktime(datetime.datetime.strptime(date_str, "%Y-%m-%d").timetuple())  
    
def convert_fn(input):
    if input=="null":
        return np.NaN
    else:
        return float(input)
    
def historical_data(symbol, start_date, end_date):
    col_names = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    converter = {}
    for el in col_names:
        converter[el] = convert_fn
        
    token = refresh_token()
    data = (int(str_to_timestamp(start_date)),int(str_to_timestamp(end_date)),token["crumb"])
    
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + symbol + "?period1={0}&period2={1}&interval=1d&events=history&crumb={2}".format(*data)
    
    data = requests.get(url, cookies={'B':token["cookie"]})
    buf = io.StringIO(data.text) # create a buffer
    df = pd.read_csv(buf,index_col=0,converters=converter,parse_dates=True) # convert to pandas DataFrame
    return df