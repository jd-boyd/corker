from setuptools import setup, find_packages

setup(name='corker',
      version='0.1.1',
      description='Another WSGI Framework',
      long_description=open('README.md').read(),
      license='BSD',
      author='Joshua D. Boyd',
      author_email='jdboyd@jdboyd.net',
      url='https://github.com/jd-boyd/corker',
      packages=find_packages(),
      install_requires=['webob', 'routes'],
      tests_require=['nose', 'webtest'],
     )
