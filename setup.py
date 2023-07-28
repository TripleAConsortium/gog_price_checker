from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gog_price_checker",
    version="0.1.9",
    author="Alex",
    author_email="iampopovich@example.com",
    description="A tool to check game prices from GOG API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iampopovich/gog_price_checker",
    packages=["gog_price_checker"],
    entry_points={
        "console_scripts": [
            "gog_price_checker = gog_price_checker.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
