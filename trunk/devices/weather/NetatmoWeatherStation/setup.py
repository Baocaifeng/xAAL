from setuptools import setup,find_packages

with open('README.rst') as f:
    long_description = f.read()

VERSION = "0.1"

setup(
    name="xaal.netatmo",
    version=VERSION,
    license='GPL License',
    author='Caifeng BAO',
    author_email='caifeng.bao@imt-atlantique.fr',
    #url='',
    description=('xAAL devices for Netatmo Weather Station' ),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['xaal', 'netatmo','weather','station'],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'xaal.lib',
        #'requests',
        #'json'
    ]
)
