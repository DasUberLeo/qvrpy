import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='qvrpy',  
    version='0.1',
    author="Grant Patterson",
    author_email="patterson.grant@gmail.com",
    description="An abstraction of the QVR Pro API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['QVR Pro', 'QVRPro', 'QNAP', 'IoT', 'Surveillance'],
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
