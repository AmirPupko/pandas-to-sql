from pandas_to_sql.engine.columns.column import Column


class TimestampColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='TIMESTAMP', sql_string=sql_string)
