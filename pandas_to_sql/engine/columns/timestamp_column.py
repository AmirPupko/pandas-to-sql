from datetime import timedelta 
from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.common import add_comparison_operators_to_class, value_to_sql_string

class TimestampColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='TIMESTAMP', sql_string=sql_string)
    

def __my_add__(col, v):
        if not isinstance(v, timedelta):
            raise Exception(f'Supporting only timedelta, got {str(type(r))}')
        
        added_days = f"'+{v.days} days'"
        added_seconds = f"'+{v.seconds} seconds'"
        sql_string = f"(datetime({value_to_sql_string(col)}, {added_days}, {added_seconds}))"
        return TimestampColumn(sql_string=sql_string)  


add_comparison_operators_to_class(TimestampColumn)

TimestampColumn.__add__ = __my_add__
TimestampColumn.__radd__ = lambda self, l: __my_add__(self, l)