from setuptools import find_packages, setup

setup(
    name="spellingbee",
    version="1.0",
    packages=find_packages(),
    license="Private",
    description="Spelling bee for Kids on Mac",
    author="sukhbinder",
    author_email="sukh2010@yahoo.com",
    entry_points={
        'console_scripts': [' spelling = spellingbee:main',
        'spelling_log = spellingbee:showlog'],
    }
)
