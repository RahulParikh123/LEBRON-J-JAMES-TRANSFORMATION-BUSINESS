"""
Setup script for the Enterprise Data Transformation Platform
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="data-transformation-platform",
    version="0.1.0",
    author="Your Name",
    description="Enterprise Data Transformation Platform for LLM Training",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pyarrow>=12.0.0",
        "openpyxl>=3.1.0",
        "python-pptx>=0.6.21",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.21.0",
        "recordlinkage>=0.16.0",
        "presidio-analyzer>=2.2.0",
        "presidio-anonymizer>=2.2.0",
        "spacy>=3.5.0",
        "psycopg2-binary>=2.9.0",
        "pymysql>=1.1.0",
        "boto3>=1.28.0",
        "dask>=2023.8.0",
        "ray>=2.6.0",
        "tqdm>=4.66.0",
        "python-dotenv>=1.0.0",
        "loguru>=0.7.0",
    ],
    entry_points={
        "console_scripts": [
            "data-transform=main:main",
        ],
    },
)

