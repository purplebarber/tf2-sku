from setuptools import setup, find_packages

setup(
    name='tf2-sku-to-name',
    version='1.0.0',
    author='Purple Barber',
    description="A python library that parses TF2 item SKU to the item's name and vice versa.",
    url='https://github.com/purplebarber/tf2-sku',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    keywords="tf2, tf2-sku, team fortress 2"
)
