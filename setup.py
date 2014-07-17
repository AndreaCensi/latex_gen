from setuptools import setup, find_packages

setup(name='LaTeXGen',
        author="Andrea Censi",
        author_email="censi@mit.edu",
        version="0.6",
        package_dir={'':'src'},
        packages=find_packages('src'),
        entry_points={
         'console_scripts': [
            'latex_gen_demos = latex_gen.tests.demos:main',
         ]
        },
        install_requires=[],
        extras_require={},
)

