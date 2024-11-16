from setuptools import setup, find_packages

setup(
    name='smartapi_login',
    version='1.0.0.1',
    description='A library for interacting with SmartAPI for historical data, trading sessions, and more.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Mahesh Kumar',
    author_email='maheshrajbhar90@gmail.com',
    url='https://github.com/maheshrajbhar90/auto-smartapi.git',
    packages=find_packages(),
    
    install_requires=[
        'pandas>=1.0.0',
        'requests>=2.0.0',
        'pytz>=2020.1',
        'pyotp>=2.0.0',
        'SmartApi @ git+https://github.com/maheshrajbhar90/auto-smartapi.git',  # Example for private GitHub repo
    ],
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    
    python_requires='>=3.6',
    include_package_data=True,
    
    entry_points={
        "console_scripts": [
            "smartapi_login=smartapi_login:SmartAPI.run",  # Assuming SmartAPI is a class with a 'run' method
        ],
    },
)
