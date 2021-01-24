import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aplhlth", # Replace with your own username
    version="0.0.1",
    author="Brian Vegetabile",
    author_email="bvegetabile@gmail.com",
    description="Analysis of Apple Health Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bvegetabile/aplhlth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)