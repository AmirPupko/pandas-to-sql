from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.common import add_comparison_operators_to_class, value_to_sql_string
from pandas_to_sql.engine.columns.numeric_columns import IntColumn, FloatColumn

time_unit_to_format = {
    'second': '%S',
    'month': '%m',
    'minute': '%M',
    'hour': '%H',
    'week': '%W',
    'year': '%Y',
    'day': '%d',
    'dayofweek': '%w'}


class TimestampColumn(Column):

    def __init__(self, sql_string):
        super().__init__(dtype='TIMESTAMP', sql_string=sql_string)

    def __getattribute__(self, attr):
        if attr == 'dt':
            return self
        if attr == 'dayofweek':
            return self.extract_dayofweek()
        if attr in time_unit_to_format.keys():
            return self.extract_time_unit(time_unit_to_format[attr])

        return object.__getattribute__(self, attr)


    def get_sql_for_format(self, format):
        return f"(CAST(strftime('{format}', {value_to_sql_string(self)}) AS INT))"
    
    def extract_time_unit(self, format):
        sql_string = self.get_sql_for_format(format)
        return IntColumn(sql_string=sql_string)
    
    def extract_dayofweek(self):
        sql_string = self.get_sql_for_format(time_unit_to_format['dayofweek'])
        sql_string = f"( ({sql_string} + 6) % 7)"
        return IntColumn(sql_string=sql_string)


def __my_add__(col, v):
    if isinstance(v, timedelta):
        # https://docs.python.org/3/library/datetime.html#datetime.timedelta
        sign = '+' if v.days >= 0 else '-'
        added_days = f"'{sign}{abs(v.days)} days'"

        sign = '+' if v.seconds >= 0 else '-'
        added_seconds = f"'{sign}{abs(v.seconds)} seconds'"

        sql_string = f"(datetime({value_to_sql_string(col)}, {added_days}, {added_seconds}))"
        return TimestampColumn(sql_string=sql_string)
    elif isinstance(v, relativedelta):
        s = []
        for t_type, t_value in v.kwds.items():
            sign = '+' if t_value >= 0 else '-'
            s.append(f"'{sign}{abs(t_value)} {t_type}'")
        sql_string = f"(datetime({value_to_sql_string(col)}, {', '.join(s)}))"
        return TimestampColumn(sql_string=sql_string)
    elif isinstance(v, pd.offsets.DateOffset):
        s = []
        for t_type, t_value in v.kwds.items():
            sign = '+' if t_value >= 0 else '-'
            s.append(f"'{sign}{abs(t_value)} {t_type}'")
        sql_string = f"(datetime({value_to_sql_string(col)}, {', '.join(s)}))"
        return TimestampColumn(sql_string=sql_string)
    else:
        raise Exception(f'Supporting only timedelta, got {str(type(v))}')


add_comparison_operators_to_class(TimestampColumn)

TimestampColumn.__add__ = __my_add__
TimestampColumn.__radd__ = lambda self, l: __my_add__(self, l)
TimestampColumn.__sub__ = lambda self, r: __my_add__(self, -r)

