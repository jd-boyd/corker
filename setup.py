from setuptools import setup, find_packages

setup(name='corker',
      version='0.2-pre1',
      description='Another WSGI Framework',
      license='BSD',
      author='Joshua D. Boyd',
      author_email='jdboyd@jdboyd.net',
      url='https://github.com/jd-boyd/corker',
      packages=find_packages(),
      package_data={'': ['README', 'LICENSE.txt']},
      install_requires=['webob', 'routes'],
      tests_require=['nose', 'webtest'],
     )
