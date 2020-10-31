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

def numeric_op_result_from_types(l_type, r_type):
    if not is_numeric_type(l_type) or not is_numeric_type(r_type):
        raise Exception(f"supporting only numerics")
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

def get_add_op_res_type(l_type, r_type):
    if l_type == 'INT' and r_type == 'INT': return 'INT'
    elif l_type == 'VARCHAR' and r_type == 'VARCHAR': return 'VARCHAR'
    elif is_numeric_type(l_type) and is_numeric_type(r_type): return 'FLOAT'
    else: raise Exception(f"add not supprting received types. received: left type: {l_type}, right type: {r_type}")

# def get_sub_op_res_type(l_type, r_type):
#     if not is_numeric_type(l_type) or not is_numeric_type(r_type):
#         raise Exception(f"sub supporting only numerics and dates")
#     return numeric_op_result_from_types(l_type, r_type)

def get_mul_op_res_type(l_type, r_type):
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
        l_type = get_type(self)
        r_type = get_type(r)
        result_column_type = get_add_op_res_type(l_type, r_type)
        op = '||' if result_column_type == 'VARCHAR' else '+'
        return create_column_from_operation(self, r, result_column_type, op)

    def __radd__(self, l):
        l_type = get_type(l)
        r_type = get_type(self)
        result_column_type = get_add_op_res_type(l_type, r_type)
        op = '||' if result_column_type == 'VARCHAR' else '+'
        return create_column_from_operation(l, self, result_column_type, op)

    def __sub__(self, r):
        l_type = get_type(self)
        r_type = get_type(r)
        result_column_type = numeric_op_result_from_types(l_type, r_type)
        return create_column_from_operation(self, r, result_column_type, '-')

    def __rsub__(self, l):
        l_type = get_type(l)
        r_type = get_type(self)
        result_column_type = numeric_op_result_from_types(l_type, r_type)
        return create_column_from_operation(l, self, result_column_type, '-')

    def __mul__(self, r):
        l_type = get_type(self)
        r_type = get_type(r)
        result_column_type = get_mul_op_res_type(l_type, r_type)
        return create_column_from_operation(self, r, result_column_type, '*')
    
    def __rmul__(self, l):
        l_type = get_type(l)
        r_type = get_type(self)
        result_column_type = get_mul_op_res_type(l_type, r_type)
        return create_column_from_operation(l, self, result_column_type, '*')

    def __truediv__(self, r):
        l_type = get_type(self)
        r_type = get_type(r)
        # if l_type=='INT' and r_type=='INT':
        #     raise Exception('truediv not supporting 2 int columns. try converting one of the columns to float')
        # result_column_type =  #numeric_op_result_from_types(l_type, r_type)
        return create_column_from_operation(self, r, 'FLOAT', '/')
    
    def __rtruediv__(self, l):
        l_type = get_type(l)
        r_type = get_type(self)
        # if l_type=='INT' and r_type=='INT':
        #     raise Exception('truediv not supporting 2 int columns. try converting one of the columns to float')
        result_column_type = numeric_op_result_from_types(l_type, r_type)
        return create_column_from_operation(l, self, result_column_type, '/')

    def __floordiv__(self, l):
        # cast ( x as int ) - ( x < cast ( x as int ))
        l_type = get_type(l)
        r_type = get_type(self)
        # if l_type=='INT' and r_type=='INT':
        #     raise Exception('truediv not supporting 2 int columns. try converting one of the columns to float')
        # result_column_type = get_sub_op_res_type(l_type, r_type)
        return create_column_from_operation(l, self, 'FLOAT', '/')

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
    
    def __abs__(self):
        t = get_type(self)
        if not is_numeric_type(t):
            raise Exception(f'abs support only numeric columns, got: {str(t)}')
        return Column(dtype=t,
                    sql_string=f'ABS({value_to_sql_string(self)})',
                    is_direct_column=False)  
       



