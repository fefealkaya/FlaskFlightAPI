from setuptools import setup, find_packages

setup(
    name='flaskairlinecompanyapi',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Faker==18.3.1',
        'Flask==1.1.2',
        'Flask_SQLAlchemy==2.4.3',
        'flask_swagger==0.2.14'
    ],
)