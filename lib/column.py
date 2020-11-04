import numbers
import operator

NUMERIC_COLUMNS_TYPES = ['INT','FLOAT']

def get_type(v):
    if isinstance(v, Column): return v.dtype
    elif isinstance(v, str): return 'VARCHAR'
    elif isinstance(v, int): return 'INT'
    elif isinstance(v, numbers.Number): return 'FLOAT'
    else: raise Exception(f"Value not supported. supporting: premitives and {str(Column)}. got {str(type(v))}")

def is_numeric_type(v_type):
    return v_type in NUMERIC_COLUMNS_TYPES

def validate_numeric(l, r):
    l_type = get_type(l)
    r_type = get_type(r)
    if not is_numeric_type(l_type) or not is_numeric_type(r_type):
        raise Exception(f"supporting only numerics")

def numeric_op_result_from_types(l, r):
    validate_numeric(l, r)
    l_type = get_type(l)
    r_type = get_type(r)
    return 'INT' if l_type is 'INT' and r_type is 'INT' else 'FLOAT'

def value_to_sql_string(value):
    if isinstance(value, numbers.Number):
        return str(value)
    elif isinstance(value, str):
        return "'" + value + "'"
    elif isinstance(value, Column):
        return value.sql_string
    raise Exception(f"Value not supported. supporting: premitives and {str(Column)}. got {str(type(value))}")

def create_column_from_operation(l, r, dtype, op):
    return Column(dtype=dtype,
                    sql_string=f'({value_to_sql_string(l)} {op} {value_to_sql_string(r)})',
                    is_direct_column=False)  

def get_add_op_res_type(l, r):
    l_type = get_type(l)
    r_type = get_type(r)
    if l_type == 'INT' and r_type == 'INT': return 'INT'
    elif l_type == 'VARCHAR' and r_type == 'VARCHAR': return 'VARCHAR'
    elif is_numeric_type(l_type) and is_numeric_type(r_type): return 'FLOAT'
    else: raise Exception(f"add not supprting received types. received: left type: {l_type}, right type: {r_type}")

def get_mul_op_res_type(l, r):
    l_type = get_type(l)
    r_type = get_type(r)
    if l_type == 'INT' and r_type == 'INT': return 'INT'
    elif is_numeric_type(l_type) and is_numeric_type(r_type): return 'FLOAT'
    else: raise Exception(f"mul not supprting received types. received: left type: {l_type}, right type: {r_type}")


class Column:
    dtype = None
    sql_string = None
    is_direct_column = None
    
    def __init__(self, dtype, sql_string, is_direct_column):
        self.dtype = dtype
        self.sql_string = sql_string
        self.is_direct_column = is_direct_column
    
    def __copy__(self):
        return Column(self.dtype, self.sql_string, self.is_direct_column)

    def __add__(self, r):
        result_column_type = get_add_op_res_type(self, r)
        op = '||' if result_column_type == 'VARCHAR' else '+'
        return create_column_from_operation(self, r, result_column_type, op)

    def __radd__(self, l):
        result_column_type = get_add_op_res_type(l, self)
        op = '||' if result_column_type == 'VARCHAR' else '+'
        return create_column_from_operation(l, self, result_column_type, op)

    def __sub__(self, r):
        result_column_type = numeric_op_result_from_types(self, r)
        return create_column_from_operation(self, r, result_column_type, '-')

    def __rsub__(self, l):
        result_column_type = numeric_op_result_from_types(l, self)
        return create_column_from_operation(l, self, result_column_type, '-')

    def __mul__(self, r):
        result_column_type = get_mul_op_res_type(self, r)
        return create_column_from_operation(self, r, result_column_type, '*')
    
    def __rmul__(self, l):
        result_column_type = get_mul_op_res_type(l, self)
        return create_column_from_operation(l, self, result_column_type, '*')

    def __truediv__(self, r):
        validate_numeric(self, r)
        return Column(dtype='FLOAT',
                sql_string=f'(({value_to_sql_string(self)} + 0.0) / {value_to_sql_string(r)})',
                is_direct_column=False)  
    
    def __rtruediv__(self, l):
        validate_numeric(l, self)
        return Column(dtype='FLOAT',
                sql_string=f'(({value_to_sql_string(l)} + 0.0) / {value_to_sql_string(self)})',
                is_direct_column=False)  

    def __floordiv__(self, r):
        validate_numeric(self, r)
        # http://sqlite.1065341.n5.nabble.com/floor-help-td46158.html
        return Column(dtype='FLOAT',
                sql_string=f'( ROUND(({value_to_sql_string(self)} / {value_to_sql_string(r)}) - 0.5) )',
                is_direct_column=False)

    def __rfloordiv__(self, l):
        validate_numeric(l, self)
        # http://sqlite.1065341.n5.nabble.com/floor-help-td46158.html
        return Column(dtype='FLOAT',
                sql_string=f'( ROUND(({value_to_sql_string(l)} / {value_to_sql_string(self)}) - 0.5) )',
                is_direct_column=False)

    def __lt__(self,other):
        return create_column_from_operation(self, other, 'BOOL', '<')

    def __le__(self,other):
        return create_column_from_operation(self, other, 'BOOL', '<=')

    def __gt__(self,other):
        return create_column_from_operation(self, other, 'BOOL', '>')

    def __ge__(self,other):
        return create_column_from_operation(self, other, 'BOOL', '>=')

    def __eq__(self,other):
        return create_column_from_operation(self, other, 'BOOL', '=')

    def __ne__(self,other):
        return create_column_from_operation(self, other, 'BOOL', '<>')
    
    def __invert__(self):
        if self.dtype != 'BOOL':
            raise Exception(f'tilde support only bool columns, got: {self.dtype}')
        return Column(dtype='BOOL',
                sql_string=f'(NOT({value_to_sql_string(self)}))',
                is_direct_column=False)

    def __abs__(self):
        t = get_type(self)
        if not is_numeric_type(t):
            raise Exception(f'abs support only numeric columns, got: {str(t)}')
        return Column(dtype=t,
                    sql_string=f'ABS({value_to_sql_string(self)})',
                    is_direct_column=False)  

    def __neg__(self):
        t = get_type(self)
        sql_string = None
        if is_numeric_type(t): sql_string = f'(-({value_to_sql_string(self)}))'
        elif t == 'BOOL': sql_string = f'(NOT({value_to_sql_string(self)}))'
        else: raise Exception(f'- support only numeric and bool columns, got: {str(t)}')
        return Column(dtype=t,
                    sql_string=sql_string,
                    is_direct_column=False)  
       



