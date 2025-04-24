from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="stegopy",
    version="0.1.0",
    author="JeremyDeveloper",
    description="A deterministic, no-magic Python toolkit for hiding messages in media. Built with hyperfixation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JeremyDeveloper/stegopy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security :: Cryptography",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Pillow>=11.2.1"
    ],
    entry_points={
        "console_scripts": [
            "stegopy=stegopy.cli:main"
        ]
    },
    python_requires='>=3.7',
)