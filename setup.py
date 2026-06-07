"""
SmartClip Setup
SmartClip 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smartclip-tui",
    version="1.0.0",
    author="SmartClip Team",
    author_email="smartclip@example.com",
    description="AI-Powered Terminal Clipboard Manager with TUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smartclip-tui",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "textual>=0.41.0",
        "pyperclip>=1.8.0",
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartclip=smartclip.cli:cli",
            "sclip=smartclip.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
