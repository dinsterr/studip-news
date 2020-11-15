from setuptools import setup

setup(
    name='studip-news',
    version='1.0',
    packages=['requests', 'html2text', 'feedgen'],
    url='',
    license='',
    author='David Schrenk',
    author_email='david.schrenk@protonmail.com',
    description='Fetches the activity stream from the StudIp platfrom deployed at the University of Passau and converts it to an atom feed.'
)
