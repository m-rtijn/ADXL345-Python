from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(name="ADXL345-Python",
        version="1.0",
        description="A module to handle the i2c communication between a Raspberry Pi and a ADXL345",
        classifiers=[
            "License:: OSI Approved :: MIT License",
            "Topic :: Software Development :: Libraries",
            "Programming Language :: Python :: 2.7",
        ],
        keywords="adxl345 raspberry",
        url="https://github.com/Tijndagamer/mpu6050",
        author="MrTijn/Tijndagamer",
        author_email="tijndagamer25[at]gmail[dot]com",
        license="MIT",
        packages=["ADXL345"],
        install_requires=[
            "smbus",
        ],
        scripts=["bin/ADXL345-example"],
        zip_safe=False)
