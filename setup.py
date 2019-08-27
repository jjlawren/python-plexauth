from setuptools import setup

setup(
    name='plexauth',
    version='0.0.1',
    description='Handles the authorization flow to obtain tokens from Plex.tv via external redirection.',
    long_description='README.md',
    long_description_content_type='text/markdown',
    url='https://github.com/jjlawren/python-plexauth/',
    license='MIT',
    author='Jason Lawrence',
    author_email='jjlawren@users.noreply.github.com',
    packages=['plexauth'],
    install_requires=['aiohttp'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
