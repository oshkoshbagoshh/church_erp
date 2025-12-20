# Database Setup Guide

Complete guide for setting up PostgreSQL with psycopg2-binary for the Church ERP system.

## Prerequisites

1. **Python 3.10+** installed
2. **PostgreSQL 12+** installed and running
3. **Git** (optional, for cloning)

## Step 1: Virtual Environment Setup

### Windows
```bash
# Navigate to project directory
cd C:\Users\UFV\PycharmProjects\church_erp

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (you should see (venv) in prompt)
```

### Linux/macOS
```bash
# Navigate to project directory
cd /path/to/church_erp

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (you should see (venv) in prompt)
```

## Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
# Should see: psycopg2-binary, python-dotenv, bcrypt
```

## Step 3: PostgreSQL Installation

### Windows
1. Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and remember the postgres user password
3. Add PostgreSQL bin directory to PATH (usually automatic)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS
```bash
# Using Homebrew
brew install postgresql@15
brew services start postgresql@15
```

## Step 4: Configure Environment Variables

```bash
# Copy example file to create .env
cp .env.example .env

# Edit .env file with your settings
# Windows: notepad .env
# Linux/Mac: nano .env
```

### Required Configuration in .env:
```env
# PostgreSQL Superuser (for initial setup)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password

# Application Database
DB_NAME=church_erp
DB_USER=church_erp_user
DB_PASSWORD=your_secure_password_here
```

## Step 5: Initialize Database

```bash
# Make sure virtual environment is activated
# Run the initialization script
python scripts/init_db.py
```

This script will:
1. ✓ Create database user `church_erp_user`
2. ✓ Create database `church_erp`
3. ✓ Install PostgreSQL extensions (uuid-ossp, pgcrypto, pg_trgm, citext)
4. ✓ Create all tables from schema
5. ✓ Insert default roles (User, Staff, Admin)
6. ✓ Insert default vendor categories
7. ✓ Verify installation

## Step 6: Verify Installation

### Option 1: Using Python
```python
# Create a test script: scripts/test_connection.py
from app.database import Database
from dotenv import load_dotenv

load_dotenv()

# Test connection
Database.test_connection()
```

```bash
python scripts/test_connection.py
```

### Option 2: Using psql
```bash
# Connect to database
psql -U church_erp_user -d church_erp -h localhost

# List tables
\dt

# Check roles
SELECT * FROM roles;

# Exit
\q
```

## Project Structure

```
church_erp/
├── venv/                          # Virtual environment
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py          # Database connection pooling
│   │   └── query_helpers.py       # CRUD helper functions
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py     # User data access
│   │   └── vendor_repository.py   # Vendor data access
│   └── models/
│       ├── base.py
│       ├── user.py
│       └── vendor.py
├── database/
│   └── schema.sql                 # Complete database schema
├── scripts/
│   └── init_db.py                 # Database initialization
├── config.py                      # Application configuration
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (create from .env.example)
└── .env.example                   # Example environment file
```

## Usage Examples

### Example 1: Create a User
```python
from app.repositories import UserRepository
from app.database import Database

# Initialize database connection
Database.initialize()

# Create user
user_id = UserRepository.create_user(
    email='john@example.com',
    username='johndoe',
    password='SecurePass123!',
    first_name='John',
    last_name='Doe'
)

print(f"User created with ID: {user_id}")

# Get user
user = UserRepository.get_user_by_email('john@example.com')
print(f"User: {user['username']} - {user['email']}")

# Verify password
is_valid = UserRepository.verify_password(user, 'SecurePass123!')
print(f"Password valid: {is_valid}")
```

### Example 2: Create a Vendor
```python
from app.repositories import VendorRepository

# Create vendor with contact
vendor_id = VendorRepository.create_vendor(
    name='ABC Construction',
    category_id=1,  # General Contractor
    created_by=1,   # User ID
    legal_name='ABC Construction LLC',
    email='contact@abc.com',
    phone='555-1234',
    status='active',
    # Primary contact
    contact_name='John Smith',
    contact_email='john@abc.com',
    contact_phone='555-5678',
    contact_title='Project Manager'
)

# Search vendors
vendors = VendorRepository.search_vendors('ABC', status='active')
for vendor in vendors:
    print(f"{vendor['name']} - {vendor['category_name']}")
```

### Example 3: Using Raw SQL
```python
from app.database import Database

with Database.get_cursor() as cur:
    cur.execute("""
        SELECT v.name, vc.name as category
        FROM vendors v
        JOIN vendor_categories vc ON vc.id = v.category_id
        WHERE v.status = %s
        ORDER BY v.name
    """, ('active',))

    vendors = cur.fetchall()
    for vendor in vendors:
        print(f"{vendor['name']} - {vendor['category']}")
```

## Database Schema Overview

### Core Tables
- **users** - User accounts with authentication
- **roles** - User roles (User, Staff, Admin)
- **user_roles** - Many-to-many user-role relationship
- **user_sessions** - Active user sessions
- **password_reset_tokens** - Password reset functionality

### Vendor Tables
- **vendors** - Main vendor information
- **vendor_categories** - Vendor categorization
- **vendor_contacts** - Multiple contacts per vendor
- **vendor_addresses** - Multiple addresses per vendor
- **vendor_bank_accounts** - Banking information (encrypted)
- **vendor_documents** - Document attachments and metadata

### Audit
- **audit_logs** - Complete audit trail of all changes

## Permission System

Permissions are bitwise flags:
- `1` = VIEW
- `2` = CREATE
- `4` = EDIT
- `8` = DELETE
- `16` = ADMIN

Default roles:
- **User**: VIEW (1)
- **Staff**: VIEW + CREATE + EDIT (7)
- **Admin**: All permissions (31)

## Troubleshooting

### Connection Refused
```bash
# Check if PostgreSQL is running
# Windows
sc query postgresql-x64-15

# Linux
sudo systemctl status postgresql

# Start if not running
# Windows: Start from Services
# Linux
sudo systemctl start postgresql
```

### Authentication Failed
- Verify POSTGRES_PASSWORD in .env
- Check pg_hba.conf for authentication method
- Ensure PostgreSQL allows password authentication

### Extension Errors
```sql
-- Connect as superuser
psql -U postgres -d church_erp

-- Install extensions manually
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "citext";
```

### Database Already Exists
```bash
# Drop and recreate (WARNING: deletes all data)
psql -U postgres
DROP DATABASE church_erp;
# Then run init_db.py again
```

## Next Steps

1. **Create your first admin user** (through Python script)
2. **Build your application logic** using the repositories
3. **Set up backup schedule** (see docs/backup.md)
4. **Configure production settings** in config.py
5. **Build your custom ORM** on top of the database layer

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Support

For issues or questions:
1. Check this documentation
2. Review the code comments in repository files
3. Check PostgreSQL logs
4. Verify .env configuration
