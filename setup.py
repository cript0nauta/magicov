from setuptools import setup

setup(
    name='magicov',
    version='0.1',
    packages=['magicov',],
    license='GPLv3+',
    # long_description=open('README.txt').read(),
    install_requires=['google-pasta', 'coverage'],
    entry_points={
        'console_scripts': [
            'magicov=magicov:main'
        ]
    },
)
