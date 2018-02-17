from setuptools import setup,find_packages
import fastentrypoints

with open('README.rst') as f:
    long_description = f.read()

VERSION = "0.1"

setup(
    name='xaal.tools',
    version=VERSION,
    license='GPL License',
    author='Jerome Kerdreux',
    author_email='Jerome.Kerdreux@imt-atlantique.fr',
    #url='',
    description=('xAAL devices tools'),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['xaal', 'tools'],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,

  entry_points = {
      'console_scripts': [
          'xaal-isalive = xaal.tools.isalive:main',
          'xaal-info   = xaal.tools.info:main',
          'xaal-dumper  = xaal.tools.dumper:main',
          'xaal-tail    = xaal.tools.tail:main',
          'xaal-walker  = xaal.tools.walker:main',
          'xaal-keygen  = xaal.tools.keygen:main',
          'xaal-log     = xaal.tools.log:main',
      ],
    },
    
    install_requires=[
        'xaal.lib',
    ]
)
