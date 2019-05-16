import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="workeremazident",
    version="0.0.1",
    author="Oleh Sokolianskyi",
    author_email="oleg.sokolansky@gmail.com",
    description="A package with workers code of Webemazident",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aradqubasi/webemazident",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
