
class Column:
    dtype = None
    sql_string = None

    def __init__(self, dtype, sql_string):
        self.dtype = dtype
        self.sql_string = sql_string
    
    def __copy__(self):
        return type(self)(self.sql_string)
