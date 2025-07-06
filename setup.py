from setuptools import setup, find_packages

setup(
    name='tf2-sku-to-name',
    version='2.0.0',
    author='Purple Barber',
    description="A python library that parses TF2 item SKU to the item's name and vice versa.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/purplebarber/tf2-sku',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords="tf2, tf2-sku, team fortress 2, sku, parser",
    python_requires='>=3.6',
)
