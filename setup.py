from setuptools import setup, find_packages

setup(
    name="trading_app",
    version="1.0.0",
    author="Duncan Parker",
    author_email="quantDIY@protonmail.com",
    description="A trading application for live and historical data processing, indicators, and trading strategies.",
    packages=find_packages(),
    install_requires=[
        "websockets",        # For WebSocket communication
        "pandas",            # For data manipulation and analysis
        "numpy",             # For numerical operations
        "pytest",            # For testing the application
        "pytest-asyncio",    # For testing async functions
        "python-dotenv",     # For managing environment variables
        "requests",          # For HTTP API requests
        "setuptools",        # For packaging
    ],
    entry_points={
        "console_scripts": [
            "trading_app=trading_app.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Adjust this based on the Python version you're using
)
