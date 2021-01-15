import pandas as pd


## Types
def convert_df_type(col_type):
    if pd.api.types.is_bool_dtype(col_type): return 'BOOL'
    elif pd.api.types.is_integer_dtype(col_type): return 'INT'
    elif pd.api.types.is_numeric_dtype(col_type): return 'FLOAT'
    elif pd.api.types.is_string_dtype(col_type): return 'VARCHAR'
    elif pd.api.types.is_datetime64_any_dtype(col_type): return 'TIMESTAMP'
    else: raise Exception(f"could not convert column type. got: {str(col_type)}")


def create_schema_from_df(df):        
    schema = {}
    for col_name, col_type in df.dtypes.items():
        schema[col_name] = convert_df_type(col_type)
    return schema