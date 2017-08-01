#!/usr/bin/env python
import codecs
import json
import os
from setuptools import setup
    

package_name = "flownet"
packages  = [package_name,]
version_path = os.path.join("flownet", "_version.py")


with codecs.open(version_path) as f:
    version = '.'.join(str(e) for e in json.load(f))
with codecs.open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name = "flownet",
    version=version,
    description = "A simple flow network python library.",
    long_description = readme,
    author='Christopher Digirolamo',
    author_email = "chrisdigirolamo@gmail.com",
    url = "https://github.com/Digirolamo/FlowNet",
    download_url = "https://github.com/Digirolamo/FlowNet",
    license = "MIT License",
    packages=packages,
    package_data={
        '': ['LICENSE', 'README.md'],
        },
    package_dir={package_name: package_name},
    include_package_data=True,
    test_suite='tests',
    install_requires=['six>=1.8.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        ]
    )