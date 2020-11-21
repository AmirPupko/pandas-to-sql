
simple run:  
python main.py  

tests:  
pytest ./lib  
with console print: pytest ./lib -s  

env:  
conda env create -f environment.yml --prefix ./env  

conda activate ./env  

conda env update --prefix ./env -f environment.yml  

conda remove --prefix ./env --all  



![Python Package using Conda](https://github.com/AmirPupko/pandas-to-sql/workflows/Python%20Package%20using%20Conda/badge.svg)  
![Upload Python Package](https://github.com/AmirPupko/pandas-to-sql/workflows/Upload%20Python%20Package/badge.svg?event=deployment)  



Package:  
python setup.py sdist bdist_wheel  
python -m twine upload --repository pypi --skip-existing dist/*  
