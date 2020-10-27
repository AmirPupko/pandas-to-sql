from copy import copy

class PandasDataFrameIntercepter:
    def __init__(self, df_pandas, df_sql_convert_table):
        self.df_pandas = df_pandas
        self.df_sql_convert_table = df_sql_convert_table

    def __repr__(self):
        return self.df_pandas.__repr__()

    def __format__(self):
        return self.df_pandas.__format__()

    def __str__(self):
        return self.df_pandas.__str__()
    
    @staticmethod
    def get_attr_for_df_pandas_if_needed(obj):
        if isinstance(obj, PandasDataFrameIntercepter):
            return object.__getattribute__(obj, 'df_pandas')
        else:
            return obj

    @staticmethod
    def get_attr_for_df_sql_convert_table_if_needed(obj):
        if isinstance(obj, PandasDataFrameIntercepter):
            return object.__getattribute__(obj, 'df_sql_convert_table')
        else:
            return obj

    def __getattribute__(self, name):
        if name in ['df_pandas', 'df_sql_convert_table']:
            return object.__getattribute__(self, name)
        
        df_sql_convert_table_attr =  object.__getattribute__(self.df_sql_convert_table, name)
        if name=='get_sql_string' and hasattr(df_sql_convert_table_attr, '__call__'):
            return lambda *args, **kwargs: df_sql_convert_table_attr(*args, **kwargs)

        df_pandas_attr =  object.__getattribute__(self.df_pandas, name)
        if hasattr(df_sql_convert_table_attr, '__call__'):
            def _(*args, **kwargs):
                def __dictionary_map_values(d, func):
                    return {k: func(v) for k, v in d.items()}
                
                args_df_pandas = tuple(map(PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed, args))
                args_obj_new = tuple(map(PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed, args))
                
                kwargs_df_pandas = __dictionary_map_values(kwargs, PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed)
                kwargs_obj_new = __dictionary_map_values(kwargs, PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed)
                
                a = df_pandas_attr(*args_df_pandas, **kwargs_df_pandas)
                b = df_sql_convert_table_attr(*args_obj_new, **kwargs_obj_new)
                return PandasDataFrameIntercepter(a, b)
            return _
        else:           
            return PandasDataFrameIntercepter(df_pandas_attr, df_sql_convert_table_attr)
    
    def __getitem__(self, key):
        a = self.df_pandas[PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed(key)]
        b = self.df_sql_convert_table[PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed(key)]
        return PandasDataFrameIntercepter(a, b)
    
    def __setitem__(self, key, newvalue):
        self.df_pandas[key] = PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed(newvalue)
        self.df_sql_convert_table[key] = PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed(newvalue)
        return PandasDataFrameIntercepter(self.df_pandas, self.df_sql_convert_table)

    def __getattr__(self, attribute_name):
        print(attribute_name)
        a = self.df_pandas[attribute_name]
        b = self.df_sql_convert_table[attribute_name]
        return PandasDataFrameIntercepter(a, b)
    
    def __copy__(self):
        return PandasDataFrameIntercepter(copy(self.df_pandas), copy(self.df_sql_convert_table))
    
    def __add__(self, r):
        a = self.df_pandas + PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed(r)
        b = self.df_sql_convert_table + PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed(r)
        return PandasDataFrameIntercepter(a, b)
