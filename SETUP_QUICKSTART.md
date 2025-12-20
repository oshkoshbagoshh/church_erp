# Quick Start Guide - Church ERP Database Setup

## 🚀 Quick Setup (5 minutes)

### 1. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy and edit .env file
cp .env.example .env

# Edit these values in .env:
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=your_postgres_password
# DB_PASSWORD=your_secure_password_here
```

### 4. Initialize Database
```bash
python scripts/init_db.py
```

### 5. Test Connection
```bash
python scripts/test_connection.py
```

## ✅ You're Ready!

Your database is now set up with:
- ✓ PostgreSQL connection pooling
- ✓ User management with authentication
- ✓ Vendor management system
- ✓ Complete audit trail
- ✓ Default roles and categories

## 📚 Quick Examples

### Create a User
```python
from app.repositories import UserRepository
from app.database import Database

Database.initialize()

user_id = UserRepository.create_user(
    email='admin@church.org',
    username='admin',
    password='SecurePass123!',
    first_name='Admin',
    last_name='User'
)
```

### Create a Vendor
```python
from app.repositories import VendorRepository

vendor_id = VendorRepository.create_vendor(
    name='ABC Construction',
    category_id=1,
    created_by=1,
    email='contact@abc.com',
    phone='555-1234'
)
```

### Search Vendors
```python
vendors = VendorRepository.search_vendors('ABC')
for vendor in vendors:
    print(f"{vendor['name']} - {vendor['email']}")
```

## 📖 Full Documentation

See `docs/database_setup.md` for complete documentation.

## 🛠️ Tech Stack

- **Database**: PostgreSQL 12+ with psycopg2-binary
- **No ORM**: Direct SQL with connection pooling (build your own ORM later!)
- **Authentication**: bcrypt password hashing
- **Configuration**: python-dotenv for environment variables

## 📁 Key Files

- `app/database/connection.py` - Database connection manager
- `app/database/query_helpers.py` - CRUD helper functions
- `app/repositories/user_repository.py` - User data access
- `app/repositories/vendor_repository.py` - Vendor data access
- `database/schema.sql` - Complete database schema
- `config.py` - Application configuration

## 🔥 Next Steps

1. Build your application logic using the repositories
2. Create your custom ORM on top of the database layer
3. Add your business-specific tables to schema.sql
4. Implement your web framework (FastAPI, Flask, Django, etc.)

## ⚠️ Important Notes

- **No Flask/SQLAlchemy** - This uses pure psycopg2 for maximum control
- **Connection pooling** - Efficient database connection management
- **Prepared for your ORM** - Clean foundation to build on
- **Production-ready** - Includes security, audit logging, soft deletes

Enjoy building your Church ERP! 🏗️
