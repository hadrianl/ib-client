import xml.etree.ElementTree as ET
import influxdb
import requests
import time
from dateutil import parser
import datetime as dt
import os


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


if __name__ == "__main__":
    db_client = influxdb.InfluxDBClient('influxdb')
    db_client.create_database('index_info')
    db_client.switch_database('index_info')
    url = os.environ.get('RICURL')
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
                print(f'write points result: {ret}')
        time.sleep(60)