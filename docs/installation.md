# Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip or uv package manager (uv recommended)

## Installation Methods

### Basic Installation

For basic WITS decoding and CLI functionality:

```bash
pip install witskit  # From PyPI when published
```

### With SQL Storage Support

For time-series analysis and database storage capabilities:

```bash
pip install witskit[sql]  # Includes PostgreSQL and MySQL drivers
```

This installs additional dependencies:
- SQLAlchemy for database abstraction
- asyncpg for PostgreSQL async support
- aiomysql for MySQL async support

### Development Installation

#### Using uv (Recommended)

```bash
git clone https://github.com/Critlist/witskit
cd witskit
uv pip install -e ".[dev,sql]"  # Install with development and SQL dependencies
```

#### Using pip

```bash
git clone https://github.com/Critlist/witskit
cd witskit
pip install -e ".[dev,sql]"  # From source with development and SQL dependencies
```

## Verifying Installation

After installation, verify that WitsKit is working correctly:

```bash
witskit --version
witskit demo  # Run a quick demonstration
```

### Test SQL Storage (if installed)

If you installed the SQL support, test the database functionality:

```bash
# Test SQLite storage
echo "&&\n01083650.40\n!!" | witskit stream file:///dev/stdin --sql-db sqlite:///test.db

# Query the stored data
witskit sql-query sqlite:///test.db --list-symbols
```

## Database Setup

### SQLite

SQLite requires no additional setup - databases are created automatically:

```bash
witskit stream file://data.wits --sql-db sqlite:///drilling_data.db
```

### PostgreSQL

Install and configure PostgreSQL:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS with Homebrew
brew install postgresql

# Start PostgreSQL service
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS
```

Create a database and user:

```sql
CREATE DATABASE wits_data;
CREATE USER wits_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE wits_data TO wits_user;
```

Test connection:

```bash
witskit stream file://data.wits --sql-db postgresql://wits_user:your_password@localhost/wits_data
```

### MySQL

Install and configure MySQL:

```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# macOS with Homebrew
brew install mysql

# Start MySQL service
sudo systemctl start mysql       # Linux
brew services start mysql        # macOS
```

Create a database and user:

```sql
CREATE DATABASE wits_data;
CREATE USER 'wits_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON wits_data.* TO 'wits_user'@'localhost';
FLUSH PRIVILEGES;
```

Test connection:

```bash
witskit stream file://data.wits --sql-db mysql://wits_user:your_password@localhost/wits_data
```

## Development Setup

For development, install with all optional dependencies:

```bash
uv pip install -e ".[dev,sql,test,docs]"
```

This will install:
- Core WitsKit functionality
- SQL storage support (PostgreSQL, MySQL, SQLite)
- Development tools (black, ruff, mypy)
- Testing tools (pytest, coverage)
- Documentation tools (mkdocs, mkdocstrings)

## Troubleshooting

### Import Errors

If you get import errors related to SQL:

```python
ImportError: No module named 'asyncpg'
```

Install SQL dependencies:

```bash
pip install witskit[sql]
```

### Database Connection Issues

#### PostgreSQL Connection Refused

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -h localhost -U wits_user -d wits_data
```

#### MySQL Connection Issues

```bash
# Check if MySQL is running
sudo systemctl status mysql

# Test connection
mysql -h localhost -u wits_user -p wits_data
```

### Performance Issues

For high-volume data streaming, consider:

1. **Increase batch size**: `--sql-batch-size 1000`
2. **Use connection pooling**: Automatically handled by SQLAlchemy
3. **Optimize database**: Create appropriate indexes (done automatically)

### Memory Issues

For large datasets:

1. **Use streaming queries**: WitsKit uses async generators for memory efficiency
2. **Limit query results**: Use `--limit` parameter
3. **Time-based filtering**: Use `--start` and `--end` for focused queries
