# pandas-to-sql

## intro
Convert [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) manipulations to sql query string.


![Tests](https://github.com/AmirPupko/pandas-to-sql/workflows/Tests/badge.svg)

![Publish to PyPI](https://github.com/AmirPupko/pandas-to-sql/workflows/Publish%20to%20PyPI/badge.svg)

###
Here is an [Example Notebook](https://colab.research.google.com/drive/1A9_JWUVLYuIAVY3naynutMLqjxLKA03L?usp=sharing) 
  
 
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
