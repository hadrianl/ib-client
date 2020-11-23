import xml.etree.ElementTree as ET
import influxdb
import requests
import time
from dateutil import parser
import datetime as dt
import os
import re
from functools import reduce
import pandas as pd


def convert(raw):
    tree = ET.fromstring(raw)
    data = {}
    meta_data = {}
    index = tree.find('index')
    meta_data['datetime'] = parser.parse(index.get('datetime'))
    meta_data['code'] = index.get('code')
    meta_data['last'] = float(index.get('current'))
    meta_data['high'] = float(index.get('high'))
    meta_data['low'] = float(index.get('low'))
    constituents = data.setdefault((index.find('sname').text, index.get('code')), {})
    for s in index.find('constituents').iter(tag='stock'):
        constituents[(s.find('sname').text, s.get('code'))] = float(s.get('contribution'))

    return meta_data, data

def cv(s):
    if not isinstance(s, str):
        return s
    s2n = {'%': 0.01, '百': 100, '千': 1000, '万': 10_000, '亿': 100_000_000}
    m = re.fullmatch(r'([\+-]*[1-9][\d|,]*\.?\d*|[\+-]*0\.\d*)([%|百|千|万|亿]*)', s)

    if not m:
        return 0
        
    return float(m[1].replace(',', '')) * reduce(lambda x, y: x*y, map(s2n.get, m[2]), 1)


if __name__ == "__main__":
    host = os.environ.get('INFLUXDB_HOST', 'influxdb')
    port = os.environ.get('INFLUXDB_PORT', '8086')
    url = os.environ.get('RICURL', 'https://www.hsi.com.hk/HSI-Net/HSI-Net?cmd=nxgenindex&index=00001')
    cap_url = os.environ.get('CAPURL', 'http://www.aastocks.com/sc/stocks/market/index/hk-index-con.aspx?index=HSI&t=1&s=1&o=1&p=4&hk=0&export=1')
    db_client = influxdb.InfluxDBClient(host, int(port))
    db_client.create_database('index_info')
    db_client.switch_database('index_info')
    
    try:
        table = pd.read_html(cap_url, header=0, index_col=0, converters={i:cv for i in [3, 4, 5, 8, 9]})[0]
        points = []
        for name_code, rows in table.iterrows():
            name, code = name_code.split('  ')
            points.append({
                'measurement': 'stock_info',
                'tags': {
                    'stock_name': name,
                    'stock_code': '00' + code,
                },
                'fields': {
                    'price': rows['现价'],
                    'capital': rows['市值'],
                }
            })
        ret = db_client.write_points(points)
        print(f'write stock info points result: {ret}')
    except Exception as e:
        print(f'get stock capital failed:{e}')

    print(f'get url: {url}')
    print('begin to record index contribution!')
    while True:
        try:
            resp = requests.get(url)
        except Exception as e:
            print(f'fetch data failed: {e}')
        else:
            if resp.ok:
                meta_data, data = convert(resp.text)
                points = [
                    {
                        'measurement': 'index',
                        'time': meta_data['datetime'],
                        'tags': {
                            'code': meta_data['code'],
                        },
                        'fields': {
                            'last': meta_data['last'],
                            'high': meta_data['high'],
                            'low': meta_data['low'],
                        }

                    }
                ]
                for (index_name, index_code), cons in data.items():
                    for (stock_name, stock_code), c in cons.items():
                        point = {
                            'measurement': 'contribution',
                            'time': meta_data['datetime'],
                            'tags': {
                                'index_name': index_name,
                                'index_code': index_code,
                                'stock_name': stock_name,
                                'stock_code': stock_code,
                            },
                            'fields': {
                                'contribution': c,
                            }
                        }

                        points.append(point)

                ret = db_client.write_points(points)
                print(f'write index info points result: {ret}')
        time.sleep(60)