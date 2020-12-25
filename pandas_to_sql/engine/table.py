from copy import copy
from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.grouped_table import GroupedTable
from pandas_to_sql.engine.columns.common import get_column_class_from_type, create_column_from_value


class Table:
    table_name = None
    columns = None
    filters = None
    from_sql_string = None
    had_changed = None
    
    def __init__(self, table_name, columns, from_sql_string, filters,  had_changed):
        self.table_name = table_name
        self.columns = columns
        self.filters = filters
        self.from_sql_string = from_sql_string
        self.had_changed = had_changed

    def __getitem__(self, key):
        if isinstance(key, Column):
            if key.dtype != 'BOOL':
                raise Exception('Can only filter/where using column of type BOOL. got %s' % (key.dtype))
            return self.where(key)
        if isinstance(key, list):
            if all(map(lambda x: isinstance(x, str), key)) == False:
                raise Exception('List must be all strings. got %s' % (key))
            if all(map(lambda x: x in self.columns, key)) == False:
                raise Exception('All columns names must be a column in the table. got %s' % (key))
            return self.select(key)

        c = copy(self.columns[key])
        return c

    def __setitem__(self, key, newvalue):
        if isinstance(newvalue, Column) or issubclass(type(newvalue), Column):
            self.columns[key] = newvalue
            self.had_changed = True
        else:            
            self.columns[key] = create_column_from_value(newvalue)
            self.had_changed = True
    
    def __getattr__(self, attribute_name):
        return self[attribute_name]
    
    def __copy__(self):
        columns_copy = {}
        for c in self.columns.keys(): 
            columns_copy[c] = self[c]  # column deep copy will occur in __getitem__
        
        filters_copy = []
        for f in self.filters: filters_copy.append(copy(f))

        result_table = create_table(table_name=self.table_name,
                             from_sql_string=self.from_sql_string, 
                             had_changed=self.had_changed,
                             columns=columns_copy,
                             filters=filters_copy)
        return result_table

    def reset_index(self, level=None, drop=False, inplace=False, col_level=0, col_fill=''):
        return copy(self)
    
    def to_frame(self):
        return copy(self)

    def where(self, cond_column):
        self.had_changed = True
        new_table = copy(self)
        new_table.filters.append(cond_column)
        return new_table

    def select(self, columns_names):
        self.had_changed = True
        new_table = copy(self)
        # filter only selected columns from columns dictionary
        new_table.columns = \
            {col_name:col_val for (col_name, col_val) in new_table.columns.items() if col_name in columns_names}
        return new_table
    
    def merge(self, right, how='inner', on=None, left_on=None, right_on=None):
        if not isinstance(right, Table):
            raise Exception("merge expects right to be of type: %s, got: %s" %  (str(type(Table)), str(type(right))))
        if how not in ['left', 'inner']:
            raise Exception("merge 'how' value must be in [‘left’, ‘inner’]")

        left = copy(self)
        right = copy(right)
        if len(set(left.columns.keys()) & set(right.columns.keys())) > 1:
            raise Exception("merge got duplicates columns in both tables (except 'on' value)")
        
        left_on_column = None
        right_on_column = None
        if on and not left_on and not right_on:
            left_on_column = on
            right_on_column = on
        elif left_on and right_on and not on:
            left_on_column = left_on
            right_on_column = right_on
        else:
            raise Exception("got unexpected on/left_on/right_on values.")

        if not isinstance(left_on_column, str) or \
            not isinstance(right_on_column, str):
            raise Exception("'on/left_on/right_on' must be str")
        
        if left_on_column not in left.columns or right_on_column not in right.columns:
            raise Exception("merge 'on/left_on/right_on' value must be in both tables as column")
        
        left_columns = dict(zip(left.columns.keys(), map(lambda x: left[x], left.columns.keys())))
        right_columns = dict(zip(right.columns.keys(), map(lambda x: right[x], right.columns.keys())))

        # creating new table columns
        if left_on_column == right_on_column:
            right_columns.pop(on)
        new_table_columns = {**left_columns, **right_columns}

        # creating new table sql string
        single_select_field_format = 't1.%s AS %s'
        selected_fields_left = ', '.join(list(map(lambda x: single_select_field_format % (x, x), left_columns.keys())))
        
        single_select_field_format = 't2.%s AS %s'
        selected_fields_right = ', '.join(list(map(lambda x: single_select_field_format % (x, x), right_columns.keys())))
        
        selected_fields = selected_fields_left
        if selected_fields_right:
            selected_fields += ', ' + selected_fields_right
        
        new_table_sql_string = f'SELECT {selected_fields} FROM ({left.get_sql_string()}) AS t1 {how.upper()} JOIN ({right.get_sql_string()}) AS t2 ON t1.{left_on_column}=t2.{right_on_column}'
        
        return create_table(table_name='Temp',
                    columns=new_table_columns,
                    from_sql_string=new_table_sql_string)

    def groupby(self, by):
        def __get_column_key(col):
            for k in self.columns.keys():
                if self.columns[k].sql_string==col.sql_string: return k
            raise Exception('groupby got column that is not in table')
                
        groupings = None
        if isinstance(by, str):
            groupings = {by:self[by]}
        elif isinstance(by, Column):
            groupings = {__get_column_key(by): copy(by)}
        elif isinstance(by, list):
            groupings = {}
            for b in by:
                if isinstance(b, str): groupings[b] = self[b]
                elif isinstance(b, Column): groupings[__get_column_key(by)] = copy(b)
                else: raise Exception(f'groupby got unexpected type. expect str or column, got: {str(type(b))}')
        else:
            raise Exception("groupby 'by' value must be str OR list[str] OR Column OR list[Column]")
        
        return GroupedTable(copy(self), groupings=groupings)
        
    def get_sql_string(self):
        if self.from_sql_string and not self.had_changed:
            return self.from_sql_string
        
        from_field = None
        selected_fields = None
        if self.from_sql_string:
            from_field = f'({self.from_sql_string}) AS {self.table_name}'
        else:
            from_field = self.table_name

        single_select_field_format = '(%s) AS %s'
        selected_fields = ', '.join(list(map(lambda x: single_select_field_format % (self[x].sql_string, x), self.columns.keys())))

        single_where_field_format = '(%s)'
        where_cond = ' AND '.join(list(map(lambda c: single_where_field_format % (c.sql_string), self.filters)))
        
        if where_cond:
            return f'SELECT {selected_fields} FROM {from_field} WHERE {where_cond} '
        else:
            return f'SELECT {selected_fields} FROM {from_field}'




def create_table_from_schema(table_name, schema) -> Table:
    columns = {}
    for column_name in schema.keys():
        columns[column_name] = get_column_class_from_type(schema[column_name])(sql_string=column_name)
    return create_table(table_name=table_name, columns=columns)

def create_table(table_name, columns={}, from_sql_string=None, filters=[], had_changed=False) -> Table:
    return Table(
        table_name=table_name,
        columns=columns,
        from_sql_string=from_sql_string,
        filters=filters,
        had_changed=had_changed)