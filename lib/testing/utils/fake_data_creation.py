import pandas as pd
import numpy as np


def random_datetimes_or_dates(start, end, out_format='datetime', n=10):
    '''   
    unix timestamp is in ns by default. 
    I divide the unix time value by 10**9 to make it seconds (or 24*60*60*10**9 to make it days).
    The corresponding unit variable is passed to the pd.to_datetime function. 
    Values for the (divide_by, unit) pair to select is defined by the out_format parameter.
    for 1 -> out_format='datetime'
    for 2 -> out_format=anything else
    '''
    (divide_by, unit) = (
        10**9, 's') if out_format == 'datetime' else (24*60*60*10**9, 'D')

    start_u = start.value//divide_by
    end_u = end.value//divide_by

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit=unit)


def random_timedelta(start, end, n, unit='D', seed=None):
    if not seed:  # from piR's answer
        np.random.seed(0)

    ndays = (end - start).days + 1
    return pd.to_timedelta(np.random.rand(n) * ndays, unit=unit)


def create_fake_dataset(start=pd.to_datetime('2015-01-01'), end=pd.to_datetime('2018-01-01')):
    df = pd.DataFrame()
    df_size = 1000
    df_random_columns = {
        'random_int': 'INT',
        'random_float': 'FLOAT',
        'random_bool': 'BOOL',
        'random_datetime': 'TIMESTAMP',
        'random_str': 'VARCHAR',
    }
    df['random_int'] = np.random.randint(1, 6, df_size)
    df['random_float'] = np.random.randn(df_size)
    df['random_bool'] = np.random.randn(df_size) > 0
    df['random_datetime'] = random_datetimes_or_dates(start, end, n=df_size)
    df['random_str'] = pd.util.testing.rands_array(10, df_size)
    return df, df_random_columns
