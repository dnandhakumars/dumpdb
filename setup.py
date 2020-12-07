from setuptools import setup, find_packages
from os import path


classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Framework :: Django :: 3.0'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

 
setup(
  name='mysqldump',
  version='0.0.10',
  description='Mysqldump is a django package to import and export mysql database.',
  long_description=long_description,
  long_description_content_type = 'text/markdown',
  url='',  
  author='Nandhakumar D',
  author_email='dnandhakumars@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mysqldump, backup, restore',
  include_package_data=True,
  packages=find_packages(),
  python_requires='>=3.6',
  install_requires=['django>=3.0']
)