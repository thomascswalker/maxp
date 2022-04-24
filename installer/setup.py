setup(
    name="better-max-tools-installer",
    version="1.0.0",
    description="Installer for the Better Max Tools Python package.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/thomascswalker/better-max-tools",
    author="Thomas Walker",
    author_email="thomascswalker@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["reader"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": ["better-max-tools-installer=installer.__main__:main"]
    },
)
