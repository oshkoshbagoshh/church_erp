"""Database initialization script."""
import psycopg
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_database():
    """Create database and user if they don't exist."""
    print("\n" + "="*60)
    print("STEP 1: Creating Database and User")
    print("="*60)

    # Connect to PostgreSQL default database
    try:
        conninfo = (
            f"host={os.getenv('DB_HOST', 'localhost')} "
            f"port={os.getenv('DB_PORT', '5432')} "
            f"dbname=postgres "
            f"user={os.getenv('POSTGRES_USER', 'postgres')} "
            f"password={os.getenv('POSTGRES_PASSWORD', '')}"
        )
        conn = psycopg.connect(conninfo, autocommit=True)
        cur = conn.cursor()
    except psycopg.Error as e:
        print(f"✗ Failed to connect to PostgreSQL: {e}")
        print("\nMake sure:")
        print("  1. PostgreSQL is installed and running")
        print("  2. POSTGRES_USER and POSTGRES_PASSWORD are set in .env")
        sys.exit(1)

    db_name = os.getenv('DB_NAME', 'church_erp')
    db_user = os.getenv('DB_USER', 'church_erp_user')
    db_password = os.getenv('DB_PASSWORD', 'your_password')

    try:
        # Create user if not exists
        print(f"\nCreating user '{db_user}'...")
        cur.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '{db_user}') THEN
                    CREATE USER {db_user} WITH PASSWORD '{db_password}';
                    RAISE NOTICE 'User created';
                ELSE
                    RAISE NOTICE 'User already exists';
                END IF;
            END
            $$;
        """)
        print(f"✓ User '{db_user}' ready")

        # Create database if not exists
        print(f"\nCreating database '{db_name}'...")
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cur.fetchone():
            cur.execute(f"""
                CREATE DATABASE {db_name}
                WITH OWNER = {db_user}
                ENCODING = 'UTF8'
                LC_COLLATE = 'en_US.UTF-8'
                LC_CTYPE = 'en_US.UTF-8'
            """)
            print(f"✓ Database '{db_name}' created")
        else:
            print(f"✓ Database '{db_name}' already exists")

        # Grant privileges
        print(f"\nGranting privileges...")
        cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}")
        print(f"✓ Privileges granted")

    except psycopg.Error as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


def install_extensions():
    """Install required PostgreSQL extensions."""
    print("\n" + "="*60)
    print("STEP 2: Installing Extensions")
    print("="*60)

    try:
        conninfo = (
            f"host={os.getenv('DB_HOST', 'localhost')} "
            f"port={os.getenv('DB_PORT', '5432')} "
            f"dbname={os.getenv('DB_NAME', 'church_erp')} "
            f"user={os.getenv('DB_USER', 'church_erp_user')} "
            f"password={os.getenv('DB_PASSWORD', '')}"
        )
        conn = psycopg.connect(conninfo, autocommit=True)
        cur = conn.cursor()
    except psycopg.Error as e:
        print(f"✗ Failed to connect to database: {e}")
        sys.exit(1)

    extensions = [
        'uuid-ossp',
        'pgcrypto',
        'pg_trgm',
        'citext'
    ]

    try:
        for ext in extensions:
            print(f"\nInstalling extension '{ext}'...")
            cur.execute(f'CREATE EXTENSION IF NOT EXISTS "{ext}"')
            print(f"✓ Extension '{ext}' installed")
    except psycopg.Error as e:
        print(f"✗ Error installing extensions: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


def run_schema_file(schema_file):
    """Execute SQL schema file."""
    print("\n" + "="*60)
    print("STEP 3: Creating Database Schema")
    print("="*60)

    if not schema_file.exists():
        print(f"✗ Schema file not found: {schema_file}")
        sys.exit(1)

    try:
        conninfo = (
            f"host={os.getenv('DB_HOST', 'localhost')} "
            f"port={os.getenv('DB_PORT', '5432')} "
            f"dbname={os.getenv('DB_NAME', 'church_erp')} "
            f"user={os.getenv('DB_USER', 'church_erp_user')} "
            f"password={os.getenv('DB_PASSWORD', '')}"
        )
        conn = psycopg.connect(conninfo)

        print(f"\nReading schema from: {schema_file}")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        print("Executing schema...")
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            conn.commit()
            print(f"✓ Schema executed successfully")

    except psycopg.Error as e:
        print(f"✗ Error executing schema: {e}")
        conn.rollback()
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)
    finally:
        conn.close()


def verify_installation():
    """Verify database installation."""
    print("\n" + "="*60)
    print("STEP 4: Verifying Installation")
    print("="*60)

    try:
        conninfo = (
            f"host={os.getenv('DB_HOST', 'localhost')} "
            f"port={os.getenv('DB_PORT', '5432')} "
            f"dbname={os.getenv('DB_NAME', 'church_erp')} "
            f"user={os.getenv('DB_USER', 'church_erp_user')} "
            f"password={os.getenv('DB_PASSWORD', '')}"
        )
        conn = psycopg.connect(conninfo)
        cur = conn.cursor()

        # Check tables
        print("\nChecking tables...")
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        print(f"✓ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        # Check roles
        print("\nChecking default roles...")
        cur.execute("SELECT name FROM roles ORDER BY id")
        roles = cur.fetchall()
        print(f"✓ Found {len(roles)} roles:")
        for role in roles:
            print(f"  - {role[0]}")

        # Check vendor categories
        print("\nChecking vendor categories...")
        cur.execute("SELECT name FROM vendor_categories ORDER BY id")
        categories = cur.fetchall()
        print(f"✓ Found {len(categories)} categories:")
        for cat in categories:
            print(f"  - {cat[0]}")

        cur.close()
        conn.close()

    except psycopg.Error as e:
        print(f"✗ Verification failed: {e}")
        sys.exit(1)


def main():
    """Main initialization function."""
    print("\n" + "="*60)
    print("   Church ERP Database Initialization")
    print("="*60)

    # Check if .env file exists
    env_file = Path(__file__).parent.parent / '.env'
    if not env_file.exists():
        print("\n⚠️  Warning: .env file not found!")
        print("Please copy .env.example to .env and configure your settings.")
        print("\nCreating .env from .env.example...")

        env_example = Path(__file__).parent.parent / '.env.example'
        if env_example.exists():
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✓ .env file created. Please edit it with your PostgreSQL credentials.")
        else:
            print("✗ .env.example not found either!")

        sys.exit(1)

    # Load environment variables again
    load_dotenv()

    # Display configuration
    print("\nConfiguration:")
    print(f"  Host: {os.getenv('DB_HOST', 'localhost')}")
    print(f"  Port: {os.getenv('DB_PORT', '5432')}")
    print(f"  Database: {os.getenv('DB_NAME', 'church_erp')}")
    print(f"  User: {os.getenv('DB_USER', 'church_erp_user')}")

    response = input("\nProceed with initialization? (y/n): ")
    if response.lower() != 'y':
        print("Initialization cancelled.")
        sys.exit(0)

    # Run initialization steps
    create_database()
    install_extensions()

    schema_file = Path(__file__).parent.parent / 'database' / 'schema.sql'
    run_schema_file(schema_file)

    verify_installation()

    print("\n" + "="*60)
    print("✅ Database initialization complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Activate virtual environment:")
    print("     Windows: venv\\Scripts\\activate")
    print("     Linux/Mac: source venv/bin/activate")
    print("  2. Install dependencies: pip install -r requirements.txt")
    print("  3. Test connection: python scripts/test_connection.py")
    print("\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Initialization cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
