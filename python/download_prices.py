"""Optional offline Twelve Data adapter. Uses an environment secret, never browser code.
Requests adjusted daily close, validates exact date alignment, and fails without substitution.
Documentation: https://twelvedata.com/docs (time_series, adjust=all).
"""
import argparse, json, os, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
import pandas as pd
from research import SYMBOLS, validate_prices


def parse_history(data, today):
    if not isinstance(data,dict) or not isinstance(data.get('values'),list):
        raise ValueError('Provider returned no history; check key, quota and plan.')
    values=data['values']
    if len({v.get('datetime') for v in values})!=len(values):
        raise ValueError('Provider returned duplicate dates.')
    rows={v['datetime']:float(v['close']) for v in values if v['datetime']<today}
    if len(rows)<600:raise ValueError('Provider supplied fewer than 600 completed observations.')
    return pd.Series(rows).sort_index()


def download(key, output, count=2000, pause=8):
    today=datetime.now(pd.Timestamp.now(tz='America/New_York').tz).strftime('%Y-%m-%d')
    series=[]
    for symbol in SYMBOLS:
        params=urlencode(dict(symbol=symbol,interval='1day',outputsize=count,order='ASC',adjust='all',apikey=key))
        try:
            with urlopen('https://api.twelvedata.com/time_series?'+params,timeout=30) as res:
                history=parse_history(json.load(res),today)
        except Exception:
            # No exception URL or vendor payload is printed, because either may contain secrets.
            raise RuntimeError(f'History request failed for {symbol}. No synthetic fallback.') from None
        history.name=symbol;series.append(history)
        print(f'Received {symbol}: {len(history)} completed rows',flush=True)
        if symbol!=SYMBOLS[-1]:time.sleep(pause)
    frame=pd.concat(series,axis=1)
    # Require matching available sessions; never silently drop dates or survivor failures.
    frame.index=pd.to_datetime(frame.index)
    frame=validate_prices(frame)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);frame.to_csv(output,index_label='date')
    output.with_suffix('.provenance.json').write_text(json.dumps(dict(provider='Twelve Data',adjust='all',symbols=SYMBOLS,requestedCount=count,retrievedAt=datetime.now(timezone.utc).isoformat(),end=frame.index[-1].strftime('%Y-%m-%d'),universe='Fixed present-day 30 assets; not point-in-time membership. Survivorship bias remains.'),indent=2))
    print(f'Saved {output}',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='data/prices.csv');p.add_argument('--count',type=int,default=2000);p.add_argument('--pause',type=float,default=8)
    a=p.parse_args();key=os.environ.get('TWELVE_DATA_API_KEY')
    if not key:p.error('Set TWELVE_DATA_API_KEY in your local environment; do not paste keys into chat.')
    if not 600<=a.count<=5000 or a.pause<0:p.error('count must be 600–5000; pause must be nonnegative.')
    download(key,a.output,a.count,a.pause)
