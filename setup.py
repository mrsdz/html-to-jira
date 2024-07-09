from setuptools import setup, find_packages

setup(
    name="html_to_jira",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "html_to_jira=html_to_jira.converter:html_to_jira",
        ],
    },
    author="MohammadReza SDZ",
    author_email="org.m.sdz@gmail.com",
    description="A package to convert HTML to Jira Wiki Markup",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mrsdz/html-to-jira",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
