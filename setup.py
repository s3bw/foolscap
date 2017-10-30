import os

from setuptools import setup, find_packages


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file('foolscap')

setup(
    name='foolscap',
    version='0.0.1',
    author='GiantsLoveDeathMetal',
    author_email='s.williamswynn.mail@gmail.com',
    packages=find_packages(
        SOURCE,
        exclude='tests',
    ),
    package_dir={'': SOURCE},
    entry_points={
        'console_scripts': [
            'fscap=cli:main',
        ]
    },
    install_requires=[],
    classifiers=[
        "Environment :: Console",
        "Operation System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=False,
    zip_safe=False,
    setup_requires=['pytest-runner'],
)
