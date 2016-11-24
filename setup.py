from setuptools import setup

version = '0.5.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'ciso8601',
    'gdal',
    'h5py>=2.3.1',
    'numpy',
    'raster-store',
    'redis',
    'scipy',
    'setuptools',
    'turn',
    ],

tests_require = [
    ]

setup(name='raster_feeder',
      version=version,
      description=("Scripts to feed and optimize "
                   "realtime temporal data into raster stores."),
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords=[],
      author='Arjan Verkerk',
      author_email='arjan.verkerk@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['raster_feeder'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
              # NRR
              'nrr-init = raster_feeder.nrr.init:main',
              'nrr-merge = raster_feeder.nrr.merge:main',
              'nrr-move = raster_feeder.nrr.move:main',
              'nrr-nowcast = raster_feeder.nrr.nowcast:main',
              'nrr-report = raster_feeder.nrr.report:main',
              'nrr-store = raster_feeder.nrr.store:main',
          ]},
      )
