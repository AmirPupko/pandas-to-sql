import numbers

NUMERIC_COLUMNS_TYPES = ['INT','FLOAT']

def get_type(v):
    if isinstance(v, Column): return v.dtype
    elif isinstance(v, str): return 'VARCHAR'
    elif isinstance(v, int): return 'INT'
    elif isinstance(v, numbers.Number): return 'FLOAT'
    else: raise Exception(f"Value not supported. supporting: premitives and {str(Column)}. got {str(type(v))}")

def is_numeric_type(v_type):
    return v_type in NUMERIC_COLUMNS_TYPES

def numeric_op_result_from_types(l_type, r_type):
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

class Column:
    dtype = None
    sql_string = None
    is_direct_column = None
    
    def __init__(self, dtype, sql_string, is_direct_column):
        self.dtype = dtype
        self.sql_string = sql_string
        self.is_direct_column = is_direct_column
    
    def __add__(self, r):
        def _add_res_type(l_type, r_type):
            if l_type == 'INT' and r_type == 'INT': return 'INT'
            elif l_type == 'VARCHAR' and r_type == 'VARCHAR': return 'VARCHAR'
            elif is_numeric_type(l_type) and is_numeric_type(r_type): return 'FLOAT'
            else: raise Exception('Columns operation not supprted. left type: %s, right type: %s' % (l.dtype, r.dtype))
        
        l_type = get_type(self)
        r_type = get_type(r)
        result_column_type = _add_res_type(l_type, r_type)
        op = '||' if result_column_type == 'VARCHAR' else '+'
        return create_column_from_operation(self, r, result_column_type, op)

    def __sub__(self, r):
        l_type = get_type(self)
        r_type = get_type(r)
        
        if not is_numeric_type(l_type) or not is_numeric_type(r_type):
            raise Exception(f"sub supporting only numerics and dates")

        result_column_type = numeric_op_result_from_types(l_type, r_type)
        return create_column_from_operation(self, r, result_column_type, '-')

    def __gt__(self, r):
        return Column(dtype='BOOL',
                      sql_string=f'({value_to_sql_string(self)} > {value_to_sql_string(r)})',
                      is_direct_column=False)

    def __copy__(self):
        return Column(self.dtype, self.sql_string, self.is_direct_column)
