from setuptools import setup, find_packages
import peeweemgr

setup(
    name="peewee-manager",
    version=peeweemgr.__version__,
    description="peewee database connection manager",
    long_description="peewee database connection manager.",
    keywords='python peewee db',
    author="mqingyn",
    url="https://github.com/mqingyn/peewee-manager",
    license="MIT",
    packages=find_packages(),
    author_email="mqingyn@gmail.com",
    requires=['peewee'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    scripts=[],
    install_requires=[
        'peewee',
    ],
)