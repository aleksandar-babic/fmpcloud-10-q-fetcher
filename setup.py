from setuptools import setup

setup(name='financestatements',
      version='1.0',
      description='Script to scrape 10-Q and 10-K statements using FMP Cloud API.',
      url='https://github.com/aleksandar-babic/fmpcloud-10-q-fetcher',
      author='Aleksandar Babic',
      author_email='contact@aleksandar-babic.com',
      license='MIT',
      packages=[
          'financestatements',
          'financestatements.FMPCloudApiClient',
          'financestatements.UserConfigParser',
          'financestatements.Utils'
      ],
      install_requires=[
          'requests',
          'pandas',
          'xlrd',
          'openpyxl',
          'xlsxwriter',
          'pyyaml'
      ],
      zip_safe=False,
      scripts=[
          'bin/finance-statements.py'
      ]
      )
