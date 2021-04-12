from setuptools import setup, find_packages

setup(name='brazil_stock_market',
      version='0.12',
      description='Scraper for assets available in brazilian Stock Exchange BM&FBOVESPA',
      url='',
      author='Leonardo Pache',
      author_email='leonardo@pache.eng.br',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)


# How to compile and install the package
# from home of project, generate the compiled structure. build/, dist/ and xxx.egg.info
# python setup.py bdist_wheel
# if everything ok, install the .whl file in dist/
# python3 -m pip install dist/xxx-0.1-py3-none-any.whl


