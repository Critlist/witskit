# Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip or uv package manager (uv recommended)

## Installation Methods

### Using uv (Recommended)

```bash
git clone https://github.com/Critlist/witskit
cd witskit
uv pip install -e ".[dev]"  # Install with development dependencies
```

### Using pip

```bash
pip install witskit  # From PyPI when published
# or
pip install -e ".[dev]"  # From source with development dependencies
```

## Verifying Installation

After installation, verify that WitsKit is working correctly:

```bash
witskit --version
```

## Development Setup

For development, install with all optional dependencies:

```bash
uv pip install -e ".[dev,test,docs]"
```

This will install:
- Development tools (black, ruff, mypy)
- Testing tools (pytest, coverage)
- Documentation tools (mkdocs, mkdocstrings)
