from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.common import add_comparison_operators_to_class, value_to_sql_string, create_column_from_operation


class FloatColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='FLOAT', sql_string=sql_string)


class IntColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='INT', sql_string=sql_string)


def __floordiv__(self, r):
    # http://sqlite.1065341.n5.nabble.com/floor-help-td46158.html
    return FloatColumn(sql_string=f'( ROUND(({value_to_sql_string(self)} / {value_to_sql_string(r)}) - 0.5) )')

def __rfloordiv__(self, l):
    # http://sqlite.1065341.n5.nabble.com/floor-help-td46158.html
    return FloatColumn(sql_string=f'( ROUND(({value_to_sql_string(l)} / {value_to_sql_string(self)}) - 0.5) )')

def is_int(v):
    return isinstance(v, int) or isinstance(v, IntColumn)

def numeric_op_result_from_types(l, r):
    x = IntColumn if is_int(l) and is_int(r) else FloatColumn
    return x

def __add__(self, r):
    res_column_type = numeric_op_result_from_types(self, r)
    return create_column_from_operation(self, r, res_column_type, '+')

def __radd__(self, l):
    res_column_type = numeric_op_result_from_types(l, self)
    return create_column_from_operation(l, self, res_column_type, '+')

def __sub__(self, r):
    res_column_type = numeric_op_result_from_types(self, r)
    return create_column_from_operation(self, r, res_column_type, '-')

def __rsub__(self, l):
    res_column_type = numeric_op_result_from_types(l, self)
    return create_column_from_operation(l, self, res_column_type, '-')

def __mul__(self, r):
    res_column_type = numeric_op_result_from_types(self, r)
    return create_column_from_operation(self, r, res_column_type, '*')

def __rmul__(self, l):
    res_column_type = numeric_op_result_from_types(l, self)
    return create_column_from_operation(l, self, res_column_type, '*')

def __truediv__(self, r):
    return FloatColumn(sql_string=f'(({value_to_sql_string(self)} + 0.0) / {value_to_sql_string(r)})')  

def __rtruediv__(self, l):
    return FloatColumn(sql_string=f'(({value_to_sql_string(l)} + 0.0) / {value_to_sql_string(self)})')  

def __abs__(self):
    return type(self)(sql_string=f'ABS({value_to_sql_string(self)})')  

def __neg__(self):
    return type(self)(sql_string=f'(-({value_to_sql_string(self)}))')


def round_(self):
    return FloatColumn(sql_string=f'(ROUND({value_to_sql_string(self)}))')



add_comparison_operators_to_class(FloatColumn)
FloatColumn.__add__ = __add__
FloatColumn.__radd__ = __radd__
FloatColumn.__sub__ = __sub__
FloatColumn.__rsub__ = __rsub__
FloatColumn.__mul__ = __mul__
FloatColumn.__rmul__ = __rmul__
FloatColumn.__floordiv__ = __floordiv__
FloatColumn.__rfloordiv__ = __rfloordiv__
FloatColumn.__truediv__ = __truediv__
FloatColumn.__rtruediv__ = __rtruediv__
FloatColumn.__abs__ = __abs__
FloatColumn.__neg__ = __neg__
FloatColumn.round = round_


add_comparison_operators_to_class(IntColumn)
IntColumn.__add__ = __add__
IntColumn.__radd__ = __radd__
IntColumn.__sub__ = __sub__
IntColumn.__rsub__ = __rsub__
IntColumn.__mul__ = __mul__
IntColumn.__rmul__ = __rmul__
IntColumn.__floordiv__ = __floordiv__
IntColumn.__rfloordiv__ = __rfloordiv__
IntColumn.__truediv__ = __truediv__
IntColumn.__rtruediv__ = __rtruediv__
IntColumn.__abs__ = __abs__
IntColumn.__neg__ = __neg__
IntColumn.round = round_
