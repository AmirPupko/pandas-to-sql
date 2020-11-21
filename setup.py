import os
import setuptools

v = os.environ['RELEASE_VERSION']
print('Version: ', v)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas-to-sql", # Replace with your own username
    version=v,
    author="Amir",
    author_email="amirpupko@gmail.com",
    description="Convert pandas dataframe manipulations to sql query string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmirPupko/pandas-to-sql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)