from setuptools import setup, find_packages

setup(
    name="caldav-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "caldav>=0.9.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "caldav-mcp=main:main",
        ],
    },
    python_requires=">=3.8",
)