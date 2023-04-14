from setuptools import setup, find_packages

setup(
    name='odacova.py',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'typing',
        'asyncio',
        'aiohttp',
    ],
)