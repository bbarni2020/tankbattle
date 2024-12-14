from setuptools import setup, find_packages  

setup(  
    name="tankbattle",  
    version="1.0.0",  
    author="Balogh Barnabás (Masterbros Developers)",  
    description="A package to simulate and visualize tank battles on a grid.",  
    long_description=open("TUTORIAL.md").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/bbarni2020/tankbattle",  
    packages=find_packages(),  
    install_requires=["tkinter"],  
    classifiers=[  
        "Programming Language :: Python :: 3",  
        "License :: Custom License (https://github.com/bbarni2020/tankbattle/LICENSE.md)",  
        "Operating System :: OS Independent",  
    ],  
    python_requires=">=3.7",  
)  
