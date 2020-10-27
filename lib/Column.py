import numbers


def get_BinOp_result_type(l, r):
    NUMERIC_COLUMNS_TYPES = ['INT','FLOAT']
    if isinstance(l, Column) and isinstance(r, Column):
        if l.dtype == 'INT' and r.dtype == 'INT': return 'INT'
        elif l.dtype in NUMERIC_COLUMNS_TYPES and r.dtype in NUMERIC_COLUMNS_TYPES: return 'FLOAT'
        elif l.dtype == 'VARCHAR' and r.dtype == 'VARCHAR': return 'VARCHAR'
        else: raise Exception('Columns operation not supprted. left type: %s, right type: %s' % (l.dtype, r.dtype))
    elif isinstance(l, Column):
        if l.dtype == 'VARCHAR' and isinstance(r, str): return 'VARCHAR'
        elif l.dtype == 'INT' and isinstance(r, int): return 'INT'
        elif l.dtype in NUMERIC_COLUMNS_TYPES and isinstance(r, numbers.Number): return 'FLOAT'
        else: raise Exception('Columns operation not supprted. left type: %s, right type: %s' % (l.dtype, type(r)))
    elif isinstance(r, Column):
        if r.dtype == 'VARCHAR' and isinstance(l, str): return 'VARCHAR'
        elif r.dtype == 'INT' and isinstance(l, int): return 'INT'
        elif r.dtype in NUMERIC_COLUMNS_TYPES and isinstance(l, numbers.Number): return 'FLOAT'
        else: raise Exception('Columns operation not supprted. left type: %s, right type: %s' % (type(l), r.dtype))
    raise Exception('No node of type Column')

def value_to_sql_string(value):
    if isinstance(value, numbers.Number):
        return str(value)
    elif isinstance(value, str):
        return "'" + value + "'"
    elif isinstance(value, Column):
        return value.sql_string
    raise Exception('value not supported')


class Column:
    dtype = None
    sql_string = None
    is_direct_column = None
    
    def __init__(self, dtype, sql_string, is_direct_column):
        self.dtype = dtype
        self.sql_string = sql_string
        self.is_direct_column = is_direct_column
    
    def __add__(self, r):
        result_column_type = get_BinOp_result_type(self, r)
        operand = '||' if result_column_type == 'VARCHAR' else '+'
        return Column(dtype=result_column_type,
                      sql_string=f'({value_to_sql_string(self)} {operand} {value_to_sql_string(r)})',
                     is_direct_column=False)

    def __gt__(self, r):
        return Column(dtype='BOOL',
                      sql_string=f'({value_to_sql_string(self)} > {value_to_sql_string(r)})',
                      is_direct_column=False)

    def __copy__(self):
        return Column(self.dtype, self.sql_string, self.is_direct_column)