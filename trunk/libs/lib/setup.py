from setuptools import setup,find_packages

with open('README.rst') as f:
    long_description = f.read()

VERSION = "0.5.001"

setup(
    name='xaal.lib',
    version=VERSION,
    license='GPL License',
    author='Jerome Kerdreux',
    author_email='Jerome.Kerdreux@imt-atlantique.fr',
    #url='',
    description=('xaal.lib is the official Python stack of xAAL protocol '
                 'dedicated to home automation systems'),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['xaal', 'home-automation'],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["ujson>=1.33","pysodium","configobj"],
)
