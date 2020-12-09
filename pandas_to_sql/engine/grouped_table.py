from copy import copy
from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.common import get_column_class_from_type

class GroupedTable:
    table = None
    groupings = None
    
    def __init__(self, table, groupings):
        self.table = table
        self.groupings = groupings

    def __copy__(self):
        return GroupedTable(copy(self.table), copy(self.groupings))

    def __getitem__(self, key):
        if isinstance(key, Column):
            raise Exception('Cant filter/where GroupedTable')
        if isinstance(key, list):
            return GroupedTable(self.table[key], copy(self.groupings))
        if isinstance(key, str):
            return GroupedTable(self.table[[key]], copy(self.groupings))
        raise Exception(f'GroupedTable __getitem__ key type not supported. type: {str(type(key))}')

    def __setitem__(self, key, newvalue):
        raise Exception(f'GroupedTable __setitem__ not supported')
        
    def __getattr__(self, attribute_name):
        return self[attribute_name]
    
    def mean(self):
        return self.agg(dict(map(lambda k: (k,'mean'),self.table.columns.keys())))

    def count(self):
        return self.agg(dict(map(lambda k: (k,'count'),self.table.columns.keys())))

    def sum(self):
        return self.agg(dict(map(lambda k: (k,'sum'),self.table.columns.keys())))

    def agg(self, v):
        if isinstance(v, str):
            return self.agg(dict(zip(self.table.columns.keys(), v)))
        elif isinstance(v, list):
            return self.agg(dict(zip(self.table.columns.keys(), v)))
        elif isinstance(v, dict):
            if len( set(v.keys()) & set(self.groupings.keys()) ) > 0:
                raise Exception("grouped table doesnt support same column in 'on' and 'select'")
            self_table_copy = copy(self.table)
            # create groupby columns query
            groupby_select_columns = {}
            for column_name in v.keys():
                column = self_table_copy[column_name]
                operations = v[column_name] if isinstance(v[column_name], list) else [v[column_name]]
                for operation in operations:
                    join_str_seperator = None
                    operation_column_name_override = None
                    dtype = None
                    
                    if callable(operation) and operation.__qualname__=='str.join':
                        join_str_seperator = operation.__self__
                        operation_column_name_override = 'join'
                        operation = 'group_concat'
#                     if not isinstance(operation, str):
#                         raise Exception(f"groupby agg support only str name for operations or ','.join. got: {type(operation)}")
#                     SUPPORTED_OPERATIONS = ['count','sum','mean','avg']
#                     if operation not in SUPPORTED_OPERATIONS:
#                         raise Exception(f"groupby operation '{operation}' is not supported. supported: {', '.join(SUPPORTED_OPERATIONS)}")

                    operation = operation.lower()
                    
                    if operation=='mean':
                        dtype = 'FLOAT'
                        operation = 'avg'
                        operation_column_name_override = 'mean'    
                    elif operation=='sum' and column.dtype=='VARCHAR':
                        dtype = 'VARCHAR'
                        operation = 'group_concat'
                        join_str_seperator = ''
                        operation_column_name_override = 'sum'
                    elif operation=='count' or (operation=='sum' and column.dtype=='INT'):
                        dtype = 'INT'
                    else:
                        dtype = 'FLOAT'
                    
                    new_column_name = f'{column_name}_{operation_column_name_override or operation}'
                    new_sql_string = f'{operation}({column.sql_string})'
                    if operation=='group_concat':
                        new_sql_string = f"{operation}({column.sql_string},'{join_str_seperator}')"
                    t = get_column_class_from_type(dtype)
                    groupby_select_columns[new_column_name] = t(sql_string=new_sql_string)
            groupby_select_columns.update(self.groupings)
            
            self_table_copy.columns = groupby_select_columns

            # create new table columns
            new_table_columns = {}
            for k in groupby_select_columns.keys():
                t = get_column_class_from_type(groupby_select_columns[k].dtype)
                new_table_columns[k] = t(sql_string=k)

            grouping_field = ', '.join(list(map(lambda k: self.groupings[k].sql_string, self.groupings.keys())))
            
            from pandas_to_sql.engine.table import create_table
            return create_table(table_name='Temp',
                         columns=new_table_columns,
                         from_sql_string=f'{self_table_copy.get_sql_string()} GROUP BY {grouping_field}',
                         had_changed=False)

