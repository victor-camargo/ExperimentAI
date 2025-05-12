# -*- encoding: utf-8 -*-
# Source: https://packaging.python.org/guides/distributing-packages-using-setuptools/

import io
import re

from setuptools import find_packages, setup

dev_requirements = [
    'bandit==1.7.5',
    'flake8==6.1.0',
    'isort==5.12.0',
    'pytest==7.4.0',
]

unit_test_requirements = [
    'coverage==7.3.0',
    'pytest==7.4.0',
    'pytest-mock==3.11.1',
    'pytest-asyncio==0.21.0',
]

integration_test_requirements = [
    *unit_test_requirements,
    'httpx==0.24.1',
]

run_requirements = [
    # REST Framework
    'fastapi',
    # Server
    'gunicorn',
    'uvicorn',
    # Logging
    'loguru',
    # Image/Array Manipulation
    'numpy',
    'Pillow',
    "opencv-python",
    "pyyaml",
    "requests",
    "scipy",
    "torch@https://download.pytorch.org/whl/cu124/torch-2.5.1%2Bcu124-cp311-cp311-linux_x86_64.whl",
    "torchvision@https://download.pytorch.org/whl/cu124/torchvision-0.20.1%2Bcu124-cp311-cp311-linux_x86_64.whl",
    # Machine Learning
    'huggingface_hub',
    'transformers',
    'accelerate',
    'datasets',
    'einops',
]


with io.open('./experimentai_api/__init__.py', encoding='utf8') as version_f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="experimentai_api",
    version=version,
    author="Victor Eduardo Ramos Camargo",
    author_email="ercamargo.victor@gmail.com",
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    url="https://github.com/victor-camargo/ExperimentAI.git",
    license="COPYRIGHT",
    description=("Esse projeto é um modelo que ..."),
    long_description=long_description,
    zip_safe=False,
    install_requires=run_requirements,
    extras_require={
        'dev': dev_requirements,
        'unit': unit_test_requirements,
        'integration': integration_test_requirements,
    },
    python_requires='==3.11.*',
    classifiers=[
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11'
    ],
    keywords=(),
    entry_points={
        'console_scripts': [
            'experimentai_api = experimentai_api.__main__:start'
        ],
    },
)
