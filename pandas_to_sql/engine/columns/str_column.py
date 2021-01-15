from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.numeric_columns import IntColumn
from pandas_to_sql.engine.columns.common import add_comparison_operators_to_class, value_to_sql_string, create_column_from_operation


class StrColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='VARCHAR', sql_string=sql_string)

    def __getattribute__(self, attr):
        if attr == 'str':
            return self
        return object.__getattribute__(self, attr)
    
    def __add__(self, r):
        return create_column_from_operation(self, r, StrColumn, '||')

    def __radd__(self, l):
        return create_column_from_operation(self, StrColumn, l, '||')


add_comparison_operators_to_class(StrColumn)

StrColumn.lower = lambda self: StrColumn(sql_string=f'(LOWER({value_to_sql_string(self)}))')
StrColumn.upper = lambda self: StrColumn(sql_string=f'(UPPER({value_to_sql_string(self)}))')

StrColumn.replace = lambda self, old, new: \
    StrColumn(sql_string=f'(REPLACE({value_to_sql_string(self)}, {value_to_sql_string(old)}, {value_to_sql_string(new)}))')


def slice_(self, start=None, stop=None,j=None):
    if j: raise 'slice "step" not supported'

    start = start if start else 0
    start+=1

    if stop:
        stop +=1
        length = stop - start
        s = f'(SUBSTR({value_to_sql_string(self)}, {start}, {length}))'
    else:
        s = f'(SUBSTR({value_to_sql_string(self)}, {start}))'

    return StrColumn(sql_string=s)


StrColumn.slice = slice_
    



def strip_(self, op, chars=None):
    if not chars:
        chars = ' '
    if not isinstance(chars, str):
        raise f'"chars" must be str. got {str(type(chars))}'
    
    s = f"({op}({value_to_sql_string(self)}, {value_to_sql_string(chars)}))"
    return StrColumn(sql_string=s)


StrColumn.strip = lambda self, chars=None: strip_(self, 'TRIM', chars)
StrColumn.lstrip = lambda self, chars=None: strip_(self, 'LTRIM', chars)
StrColumn.rstrip = lambda self, chars=None: strip_(self, 'RTRIM', chars)

StrColumn.len = lambda self: IntColumn(sql_string=f'(LENGTH({value_to_sql_string(self)}))')



def contains(self, s, case=True):
    if not isinstance(s, str):
        raise f'"s" must be str. got {str(type(s))}'
    
    if case==False:
        sql_string = f"(INSTR(LOWER({value_to_sql_string(self)}), LOWER({value_to_sql_string(s)})))"
    else:
        sql_string = f"(INSTR({value_to_sql_string(self)}, {value_to_sql_string(s)}))"
    
    # sql_string = f"(INSTR({value_to_sql_string(self)}, {value_to_sql_string(s)}))"
    sql_string = f"(CAST({sql_string} > 0 AS BOOL))"
    return StrColumn(sql_string=sql_string)


StrColumn.contains = contains
