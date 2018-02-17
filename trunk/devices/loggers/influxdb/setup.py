from setuptools import setup,find_packages

with open('README.rst') as f:
    long_description = f.read()

VERSION = "0.1"

setup(
    name='xaal.influxdb',
    version=VERSION,
    license='GPL License',
    author='Pierre-Henri Horrein',
    author_email='freki@frekilabs.fr',
    #url='',
    description=('xAAL device for InfluxDB logging' ),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['xaal', 'influxdb'],
    platforms='any',
    packages=find_packages(),
    namespace_packages=["xaal"],
    include_package_data=True,
    install_requires=[
        'xaal.lib',
        'influxdb',
    ]
)
