from setuptools import setup, find_packages

setup(
    name="task-manager",
    version="1.0.0",
    description="A simple command-line task management tool",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["main"],
    install_requires=[
        "pandas>=1.5.0",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "task-manager=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)