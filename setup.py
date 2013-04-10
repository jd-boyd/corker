from setuptools import setup, find_packages

setup(name='corker',
      version='1.0',
      description='web Framework',
      author='Joshua D. Boyd',
      author_email='jdboyd@jdboyd.net',
      url='https://github.com/jd-boyd/corker',
      packages=find_packages(),
      install_requires=['webob', 'routes'],
      tests_require=['nose', 'webtest'],
     )
