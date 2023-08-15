from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="google-sheets-to-sqlite",
    description="Create a SQLite database containing data from Google Sheets",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Théophile Cantelobre",
    url="https://github.com/theophilec/google-sheets-to-sqlite",
    project_urls={
        "Issues": "https://github.com/theophilec/google-sheets-to-sqlite/issues",
        # "CI": "https://github.com/theophilec/google-sheets-to-sqlite/actions",
        # "Changelog": "https://github.com/theophilec/google-sheets-to-sqlite/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["google_sheets_to_sqlite"],
    entry_points="""
        [console_scripts]
        google-sheets-to-sqlite=google_sheets_to_sqlite.cli:cli
    """,
    install_requires=["click", "httpx", "sqlite-utils"],
    extras_require={"test": ["pytest", "pytest-httpx", "pytest-mock", "cogapp"]},
    python_requires=">=3.6",
)
