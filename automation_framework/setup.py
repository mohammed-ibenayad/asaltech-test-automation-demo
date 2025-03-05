from setuptools import setup, find_packages

setup(
    name="automation_framework",
    version="0.1.0",
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    install_requires=[
        "selenium==4.18.1",
        "pytest==8.0.0",
        "webdriver-manager==4.0.2",
        "python-dotenv==1.0.0",
        "openai==1.12.0",
        "jinja2==3.1.3",
        "httpx==0.27.0"
    ],
    entry_points={
        'pytest11': [
            'ai_analysis = src.ai_module.pytest_plugin',
        ],
    },
)