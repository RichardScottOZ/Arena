"""
Setup configuration for the Arena package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="arena-dnd",
    version="0.1.0",
    author="Daniel R. Collins",
    author_email="dcollins@superdan.net",
    description="Python Package for Simulating Original D&D Combat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RichardScottOZ/Arena",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment :: Role-Playing",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "matplotlib>=3.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "athena=arena.athena:main",
            "arena=arena.arena:main",
        ],
    },
)
