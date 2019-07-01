import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openssl-gtk",
    version="1.0.2",
    author="Muhammed Çamsarı",
    license='MIT',
    author_email="Muhammedcamsari@icloud.com",
    description="Perform your Openssl operations without using a terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muhammedcamsari/openssl-gtk",
    keywords=['openssl', 'openssl-gui', 'security', 'encrypt'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment :: Gnome",
        "Natural Language :: Turkish",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    scripts=["openssl-gui.py"],
    packages = ['openssl_gtk'],
)