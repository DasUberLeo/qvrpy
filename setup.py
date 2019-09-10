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
    url="https://github.com/DasUberLeo/qvrpy",
    python_requires='>=3.6',
    install_requires=['requests>=2.13.0'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Home Automation",
        "Topic :: System :: Hardware"
    ],
)
