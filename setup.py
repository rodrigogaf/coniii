# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='coniii',
      version='0.1.2',
      description='CONvenient Interface to Inverse Ising',
      long_description=long_description,
      url='https://github.com/bcdaniels/coniii',
      author='Edward D. Lee, Bryan C Daniels',
      author_email='edl56@cornell.edu',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      #python_requires='==2.7',
      keywords='inverse ising maxent',
      packages=find_packages(),
      install_requires=['multiprocess','scipy','numpy','numba','dill'],
      package_data={'coniii':['setup_module.py','__init__.py']},
      exclude_package_data={'coniii':['ising_eqn/ising_eqn*.py']},
      py_modules=['coniii.exact','coniii.general_model_rmc','coniii.ising','coniii.mc_hist',
                  'coniii.mean_field_ising','coniii.pseudo_inverse_ising','coniii.samplers',
                  'coniii.solvers','coniii.utils']
)

