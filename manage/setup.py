from setuptools import setup

setup_args = dict(
    name='sopaper',
    install_requires=[
        # web framework
        'Flask>=0.9',
        'Flask-Login>=0.2.7',
        #'pyjade>=1.6',

        # database
        'pymongo>=2.6.3',

        # tool
        'sphinx>=1.1.3',
        'pep8>=1.4.6',
        'termcolor>=1.1.0',

        # network
        'beautifulsoup4>=4.3.2',
        'requests>=2.1.0',

        # pdf
        'python-magic>=0.4.6',
    ],
    entry_points=dict(
        console_scripts=[
            'api-website = standalone_server:main',
            ],
    ),
)

if __name__ == '__main__':
    setup(**setup_args)
