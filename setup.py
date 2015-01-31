from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='samsungapp',
    version=version,
    description='samsungapp',
    author='samsungapp',
    author_email='pranali.k@indictranstech.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
