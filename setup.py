import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    author="Richard Dally",
    name="bestdeal",
    version="1.0.0",
    description="Find lowest price across many vendors",
    url="https://github.com/RichardDally/BestDeal",
    license="GNU Lesser General Public License v3.0",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    author_email="r.dally@pm.me",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
