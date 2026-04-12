from setuptools import setup, find_packages

package_name = 'sensor_pipeline_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='gion',
    maintainer_email='gion@example.com',
    description='sensor pipeline python nodes',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'visualize_node = sensor_pipeline_py.visualize_node:main',
        ],
    },
)