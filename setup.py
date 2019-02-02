from setuptools import setup, find_packages


setup(
    name='crawld',
    version='0.0.9',
    description='Python website parsing engine',
    author='Leonid Lygin',
    author_email='ionagamed@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.19.1',
        'gevent==1.3.6',
        'beautifulsoup4==4.6.3'
    ]
)
