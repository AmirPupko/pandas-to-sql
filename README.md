# pandas-to-sql
**This libaray is not production ready!!**

## intro
Convert [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) manipulations to sql query string.

![Tests](https://github.com/AmirPupko/pandas-to-sql/workflows/Tests/badge.svg)

![Publish to PyPI](https://github.com/AmirPupko/pandas-to-sql/workflows/Publish%20to%20PyPI/badge.svg)

support:
 - [sqlite](https://sqlite.org/)

### try it yourself
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AmirPupko/pandas-to-sql/blob/main/pandas_to_sql_colab_example.ipynb)
Here is an [Example Notebook with Colab](https://github.com/AmirPupko/pandas-to-sql/blob/main/pandas_to_sql_colab_example.ipynb) 


## Installation
`pip install pandas-to=sql`  


## Development

### run example
`python example_runner.py`  

### tests
`pytest ./pandas_to_sql`  

### environment
`conda env create -f environment.yml --prefix ./env`  
`conda activate ./env`  
`conda env update --prefix ./env -f environment.yml`  
`conda remove --prefix ./env --all`  

### new release
`python setup.py sdist bdist_wheel`  
`python -m twine upload --repository pypi --skip-existing dist/*`  
