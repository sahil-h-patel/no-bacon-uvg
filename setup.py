from setuptools import setup

setup(
    name="nbuvg",
    version="0.1",
    py_modules=["main"],  # Your module is 'main.py'
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "nbuvg=main:cli",  # This should point to the 'cli' function in 'main.py'
        ],
    },
)
