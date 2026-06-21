"""Setup configuration for the budget_tracker package."""

from pathlib import Path

from setuptools import find_packages, setup


BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"


setup(
    name="budget-tracker-seokhun",
    version="1.0.0",
    author="seokhun",
    author_email="tjrgns@kku.ac.kr",
    description="A small household budget tracker package.",
    license="MIT",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["coverage>=7.0", "pycodestyle>=2.11", "pytest>=7.0"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
    ],
)
