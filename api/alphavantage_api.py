from datetime import datetime

from model.alphavantage_time_series import AlphavantageTimeSeries
from model.quote import Quote
from model.time_series import TimeSeries
from util.jl_utils import with_test

import requests

with open("api/alphavantage_api.key") as f:
    _key = f.read()


def _json_to_model(json):
    ats = AlphavantageTimeSeries()
    ats.key = json['Meta Data']['2. Symbol'] + ' ' +\
        json['Meta Data']['3. Last Refreshed']
    ats.json = json

    meta_data = json['Meta Data']
    ats.set(information=meta_data['1. Information'])
    ats.set(symbol=meta_data['2. Symbol'])
    ats.set(last_refreshed=meta_data['3. Last Refreshed'])
    ats.set(interval=meta_data['4. Interval'])
    ats.set(output_size=meta_data['5. Output Size'])
    ats.set(time_zone=meta_data['6. Time Zone'])

    ts_data = []
    for k, v in json[f'Time Series ({ats.interval})'].items():
        dt = datetime.strptime(k, '%Y-%m-%d %H:%M:%S')
        ts_data.append((dt, Quote(
            open=v['1. open'],
            high=v['2. high'],
            low=v['3. low'],
            close=v['4. close'],
            volume=v['5. volume'],
        )))

    ts = TimeSeries(sorted(ts_data, key=lambda x: x[0]))
    ats.set(time_series=ts)

    return ats


def api_key():
    return _key


@with_test('MSFT', apikey='demo')
def time_series_intraday(symbol, interval='1min', apikey=None):
    payload = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key() if apikey is None else apikey,
    }

    r = requests.get('https://www.alphavantage.co/query', params=payload)

    ats = _json_to_model(r.json())
    ats.save()

    return ats

