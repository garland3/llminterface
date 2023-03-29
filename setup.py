from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    description='A package that contains some Python scripts',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        # 'numpy',
        # 'pandas',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'chat=src.llm.interface_openai:main',
            # 'config=config.config:main',
        ],
    },
)
