from setuptools import setup, find_packages

setup(
    name="nbuvg",
    version="0.1",
    py_modules=["cli"],
    packages=find_packages(),  
    install_requires=[],
    install_package_data=True,
    entry_points={
        "console_scripts": [
            "nbuvg=cli:cli",
        ],
    },
)
