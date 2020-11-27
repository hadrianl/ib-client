import requests
from flask import Flask, request, session, jsonify, current_app
from influxdb import InfluxDBClient
import os
from dateutil import parser
import datetime as dt

root_url = 'https://xueqiu.com/'
minute_url = 'https://stock.xueqiu.com/v5/stock/chart/minute.json'
kline_url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

def get_hk_minute(index_name):

    if not 'component' in session:
        ic = InfluxDBClient(current_app.influx_host, current_app.influx_port)
        ic.switch_database('index_info')
        ret = ic.query("select last(contribution) from contribution where time > now() - 6h group by stock_code, stock_name")
        component = []
        for k in ret.keys():
            component.append((k[1]['stock_code'][2:-3], k[1]['stock_name']))
        session['component'] = component

    data = {}
    for s, n in session['component']:
        ret = requests.get(minute_url, params={'symbol': s, 'period': '1d'}, headers=headers, cookies=session.get('xq_cookies'))
        if ret.ok:
            data[s] = ret.json()
            data[s]['name'] = n

    return data


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1)
with app.app_context():
    current_app.influx_host = os.environ.get('INFLUXDB_HOST', 'influxdb')
    current_app.influx_port = int(os.environ.get('INFLUXDB_PORT', '8086'))


@app.before_request
def set_cookies():
    if not session.get('xq_cookies'):
        session['xq_cookies'] = requests.head(root_url, headers=headers).cookies.get_dict()

    print(session['xq_cookies'])

@app.route('/index/component/', methods=['GET'])
def get_index_component_minutes():
    index_name = request.args.get('name')

    data = get_hk_minute(index_name)

    return jsonify(data)

@app.route('/stock/minute', methods=['GET'])
def get_stock_minutes():
    stock_code = request.args.get('code')
    if not stock_code:
        return

    ret = requests.get(minute_url, params={'symbol': stock_code, 'period': '1d'}, headers=headers, cookies=session.get('xq_cookies'))
    if ret.ok:
        return jsonify(ret.json())

@app.route('/stock/kline', methods=['GET'])
def get_stock_klines():
    stock_code = request.args.get('code')
    begin = request.args.get('begin', '')
    period = request.args.get('period', '1m')
    _type = request.args.get('type', 'before')
    count = request.args.get('count', '-284')

    if not ( stock_code and begin):
        return

    if not begin.isnumeric():
        begin = int(parser.parse(begin).timestamp()*1000)

    params = {'symbol': stock_code, 'begin': begin, 'period': period, 'type': _type, 'count': count, 'indicator': 'kline'}
    ret = requests.get(kline_url, params=params, headers=headers, cookies=session.get('xq_cookies'))
    if ret.ok:
        return jsonify(ret.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0')