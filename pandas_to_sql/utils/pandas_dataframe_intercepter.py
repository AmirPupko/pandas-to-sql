from copy import copy
import operator

class PandasDataFrameIntercepter:
    def __init__(self, df_pandas, df_sql_convert_table):
        self.df_pandas = df_pandas
        self.df_sql_convert_table = df_sql_convert_table

    def __repr__(self):
        return self.df_pandas.__repr__()

    def __format__(self, fmt):
        return self.df_pandas.__format__(fmt)

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
        
        df_sql_convert_table_attr =  self.df_sql_convert_table.__getattribute__(name)
        if name=='get_sql_string' and hasattr(df_sql_convert_table_attr, '__call__'):
            return lambda *args, **kwargs: df_sql_convert_table_attr(*args, **kwargs)

        df_pandas_attr =  self.df_pandas.__getattribute__(name)
        if name=='columns' and not hasattr(df_pandas_attr, '__call__'):
            return df_pandas_attr
              
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
        a = self.df_pandas[attribute_name]
        b = self.df_sql_convert_table[attribute_name]
        return PandasDataFrameIntercepter(a, b)
    
    def __copy__(self):
        return PandasDataFrameIntercepter(copy(self.df_pandas), copy(self.df_sql_convert_table))
    
    @staticmethod
    def run_operation_and_return(left, right, op):
        left_ = PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed(left)
        right_ = PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed(right)
        a = op(left_, right_)

        left_ = PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed(left)
        right_ = PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed(right)
        b = op(left_, right_)
        return PandasDataFrameIntercepter(a, b)

    @staticmethod
    def run_operation_single_and_return(obj, op):
        a = PandasDataFrameIntercepter.get_attr_for_df_pandas_if_needed(obj)
        b = PandasDataFrameIntercepter.get_attr_for_df_sql_convert_table_if_needed(obj)
        a = op(a)
        b = op(b)
        return PandasDataFrameIntercepter(a, b)
    
    # comparisons
    def __lt__(self,other):
        return PandasDataFrameIntercepter.run_operation_and_return(self, other, operator.lt)

    def __le__(self,other):
        return PandasDataFrameIntercepter.run_operation_and_return(self, other, operator.le)

    def __gt__(self,other):
        return PandasDataFrameIntercepter.run_operation_and_return(self, other, operator.gt)

    def __ge__(self,other):
        return PandasDataFrameIntercepter.run_operation_and_return(self, other, operator.ge)

    def __eq__(self,other):
        return PandasDataFrameIntercepter.run_operation_and_return(self, other, operator.eq)

    def __ne__(self,other):
        return PandasDataFrameIntercepter.run_operation_and_return(self, other, operator.ne)

    def __abs__(self):
        return PandasDataFrameIntercepter.run_operation_single_and_return(self, operator.abs)
        
    def __neg__(self):
        return PandasDataFrameIntercepter.run_operation_single_and_return(self, operator.neg)

    def __invert__(self):
        return PandasDataFrameIntercepter.run_operation_single_and_return(self, operator.invert)

    def __contains__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.contains)

    # numeric 
    def __add__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.add)
    
    def __sub__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.sub)
    
    def __mul__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.mul)
    
    # def __matmul__(self, r):
    #     return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.matmul)

    def __truediv__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.truediv)
    
    def __floordiv__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.floordiv)
    
    def __mod__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.mod)
    
    def __pow__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.pow)
    
    def __and__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.and_)
    
    def __or__(self, r):
        return PandasDataFrameIntercepter.run_operation_and_return(self, r, operator.or_)

    # numeric r
    def __radd__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.add)
    
    def __rsub__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.sub)
    
    def __rmul__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.mul)
    
    def __rmatmul__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.matmul)

    def __rtruediv__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.truediv)
    
    def __rfloordiv__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.floordiv)
    
    def __rmod__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.mod)
    
    def __rpow__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.pow)
    
    def __rand__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.and_)
    
    def __ror__(self, l):
        return PandasDataFrameIntercepter.run_operation_and_return(l, self, operator.or_)
  
    
    
    
