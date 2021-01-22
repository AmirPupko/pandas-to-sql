
# pandas-to-sql
**This libaray is not production ready!!**

## Intro
Convert [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) manipulations to sql query string.

![Tests](https://github.com/AmirPupko/pandas-to-sql/workflows/Tests/badge.svg)

![Publish to PyPI](https://github.com/AmirPupko/pandas-to-sql/workflows/Publish%20to%20PyPI/badge.svg)

Support:
 - [sqlite](https://sqlite.org/)

### Try it yourself

```python
>>> import pandas as pd
>>> import pandas_to_sql
>>> iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
>>> df = pandas_to_sql.wrap_df(iris,  table_name='iris')
>>> df.get_sql_string()
'SELECT (sepal_length) AS sepal_length, (sepal_width) AS sepal_width, (petal_length) AS petal_length, (petal_width) AS petal_width, (species) AS species FROM iris'
```

```python
>>> df[df.species == 'setosa'].get_sql_string()
"SELECT (sepal_length) AS sepal_length, (sepal_width) AS sepal_width, (petal_length) AS petal_length, (petal_width) AS petal_width, (species) AS species FROM iris WHERE ((species = 'setosa')) "
```

[Here are some more examples](https://github.com/AmirPupko/pandas-to-sql/blob/main/pandas_to_sql_colab_example.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AmirPupko/pandas-to-sql/blob/main/pandas_to_sql_colab_example.ipynb)


## Installation
`pip install pandas-to=sql`  


## Development

### Run example
`python example_runner.py`  

### Tests
`pytest ./pandas_to_sql`  

### Environment
`conda env create -f environment.yml --prefix ./env`  
`conda activate ./env`  
`conda env update --prefix ./env -f environment.yml`  
`conda remove --prefix ./env --all`  

### New release
`python setup.py sdist bdist_wheel`  
`python -m twine upload --repository pypi --skip-existing dist/*`  
