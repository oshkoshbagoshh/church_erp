"""Test database connection script."""
from app.database import Database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Test database connection."""
    print("\n" + "="*60)
    print("   Testing Database Connection")
    print("="*60 + "\n")

    # Initialize and test connection
    try:
        Database.initialize()
        success = Database.test_connection()

        if success:
            print("\n" + "="*60)
            print("✅ Connection test passed!")
            print("="*60 + "\n")
        else:
            print("\n" + "="*60)
            print("❌ Connection test failed!")
            print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
    finally:
        Database.close_all_connections()

if __name__ == '__main__':
    main()
