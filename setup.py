from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lazym",
    version="0.16.0",
    author="Amo Chen",
    author_email="chimerhapsody@gmail.com",
    description="A tool to generate commit messages using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spitfire-sidra/lazym",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "langchain==0.3.3",
        "langchain-community==0.3.2",
        "langchain-core==0.3.10",
        "langchain-ollama==0.2.0",
        "langchain-groq==0.2.0",
        "langchain-text-splitters==0.3.0",
        "beaupy==3.9.2",
        "prompt_toolkit==3.0.48",
        "pyperclip==1.9.0",
        "halo==0.0.31"
    ],
    entry_points={
        "console_scripts": [
            "lazym=lazym.cli:main",
        ],
    },
    package_data={
        'lazym': ['prepare-commit-msg'],
    },
    include_package_data=True,
)
