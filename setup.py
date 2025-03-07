from setuptools import setup, find_packages

setup(
    name="nbuvg",
    version="0.1",
    packages=find_packages(),  # Automatically find the package
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "nbuvg=nbuvg.main:cli",  # Use the correct package name
        ],
    },
)
