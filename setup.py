from setuptools import setup

setup(
    name='regional-analysis',
    version='0.1.0',
    py_modules=['regional-analysis'],
    install_requires=[
        'et-xmlfile==1.1.0',
        'ipfn==1.4.4',
        'numpy==1.26.2',
        'openpyxl==3.0.10',
        'pandas==1.5.2',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'setuptools==68.0.0',
        'six==1.16.0',
        'wheel==0.41.2'
    ],
    entry_points={
        'console_scripts': [
            'analisis-IO-modules = regional-analysis:analisis-IO-modules',
            'analisis-LQ-modules = regional-analysis:analisis-LQ-modules',
            'analisis-SS-modules = regional-analysis:analisis-SS-modules',
            'updating-IO-modules = regional-analysis:updating-IO-modules'
        ],
    },
)
