from setuptools import setup

version = '0.3.1'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'openradar',
    'h5py',
    'matplotlib',
    'numpy',
    'PIL',
    'pydap',
    'pytz',
    'rpy2',
    'scipy',
    'setuptools',
    ],

tests_require = [
    ]

setup(name='openradar',
      version=version,
      description="TODO",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords=[],
      author='TODO',
      author_email='TODO@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['openradar'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
              'sandbox = openradar.scripts.sandbox:main',
          ]},
      )
