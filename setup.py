from setuptools import setup, find_packages

setup(name='LaTeXGen',
        author="Andrea Censi",
        author_email="andrea@cds.caltech.edu",
        version="0.5",
        package_dir={'':'src'},
        packages=find_packages('src'),
        entry_points={
         'console_scripts': [ 
           ]
        },
        install_requires=[],
        extras_require={},
)

