"""
Setup configuration for Talk-Less
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="talk-less",
    version="0.1.0",
    description="Open-source, public-good AI-assisted news platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Talk-Less Contributors",
    url="https://github.com/UnaverageDeveloper/Talk-Less",
    license="AGPL-3.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    extras_require={
        "dev": [
            line.strip()
            for line in open("requirements-dev.txt").readlines()
            if line.strip() and not line.startswith("#")
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Text Processing",
    ],
)
