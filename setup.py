from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

VERSION="0.0.6"

setup(
    name='plexauth',
    version=VERSION,
    description='Handles the authorization flow to obtain tokens from Plex.tv via external redirection.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jjlawren/python-plexauth/',
    license='MIT',
    author='Jason Lawrence',
    author_email='jjlawren@users.noreply.github.com',
    platforms='any',
    py_modules=['plexauth'],
    install_requires=['aiohttp'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
