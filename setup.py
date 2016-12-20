"""Setup/install the software"""

from setuptools import setup

setup(
    name='pypic',
    version='0.1.0',
    packages=['main', 'storage', 'cameracontroller'],
    install_requires=['azure-storage'],
    entry_points={
        'console_scripts': [
            'pypic = app.app:main'
        ]
    }
)
