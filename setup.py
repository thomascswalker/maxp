import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="better-max-tools-thomascswalker",
    version="0.0.1",
    author="Thomas Walker",
    author_email="thomascswalker@gmail.com",
    description="Better versions of standard 3ds Max tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomascswalker/better-max-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)