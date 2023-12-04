from setuptools import find_packages, setup

package_name = 'tku_libs'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='iclab',
    maintainer_email='iclab@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bbb = tku_libs.bbb:main',
            'aaa = tku_libs.aaa:main',
            # 'TKU_tool = tku_libs.TKU_tool:main'
        ],
    },
)
