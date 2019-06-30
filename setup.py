import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openssl-gtk",
    version="0.1.beta1",
    author="Muhammed Çamsarı",
    license='MIT',
    author_email="Muhammedcamsari@icloud.com",
    description="Perform your Openssl operations without using a terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhammedcamsari/openssl-gtk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["openssl-gui.py"],
    packages = ['openssl_gtk'],
)