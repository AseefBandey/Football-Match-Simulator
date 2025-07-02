from setuptools import setup, find_packages

setup(
    name="football_simulator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
        "tqdm>=4.65.0",
        "questionary>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "football-sim=football_simulator.cli:main",
        ],
    },
    author="Your Name",
    description="A football match simulator with realistic match generation",
    keywords="football, simulator, sports",
    python_requires=">=3.7",
) 