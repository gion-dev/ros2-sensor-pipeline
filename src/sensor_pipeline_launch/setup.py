from setuptools import setup, find_packages
from glob import glob
import os

package_name = 'sensor_pipeline_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='gion',
    maintainer_email='gion@example.com',
    description='launch files',
    license='Apache License 2.0',
)