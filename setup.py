from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Python wrapper for the mangadex API'
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


#setting up
setup(
    name = 'mangadex',
    version = VERSION,
    author = "Eduardo Ceja",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = ["requests", "urllib"],
    license = "MIT",
    keywords = ['python', 'mangadex'],
    clasifiers = [
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Programming Languaje :: Python :: 3.6",
        "Programming Languaje :: Python :: 3.7",
        "Programming Languaje :: Python :: 3.8",
        "Programming Languaje :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Library",
        "Topic :: Wrapper"
        ]

)