from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mysqldump',
  version='0.0.3',
  description='Mysqldump is a django package that is used to generate the logical backup of the MySQL database',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Nandhakumar D',
  author_email='dnandhakumars@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mysqldump', 
  include_package_data=True,
  packages=find_packages(),
  install_requires=['django>=3.0']
)