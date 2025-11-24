from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="agentic_learning",
    version="0.1.0",
    packages=["agentic_learning"] + ["agentic_learning." + pkg for pkg in find_packages(exclude=["tests"])],
    package_dir={"agentic_learning": "."},
    install_requires=requirements,
    python_requires=">=3.10",
)
