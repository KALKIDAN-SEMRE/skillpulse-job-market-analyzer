"""
Day 1 Verification & Testing Script
Run this script to verify your Day 1 implementation.

Usage: python test_day1.py
"""
import os
import sys
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

print("API ID:", os.getenv("TELEGRAM_API_ID"))
print("API HASH:", os.getenv("TELEGRAM_API_HASH"))


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_pass(message):
    """Print a pass message."""
    print(f"✅ PASS: {message}")


def print_fail(message):
    """Print a fail message."""
    print(f"❌ FAIL: {message}")


def print_info(message):
    """Print an info message."""
    print(f"ℹ️  INFO: {message}")


def check_structure():
    """Test 1: Check project structure."""
    print_header("1️⃣  STRUCTURE & SETUP TEST")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/database.py",
        "app/models.py",
        "app/collector.py",
        "app/extractor.py",
        "requirements.txt",
        "README.md",
        "run_collector.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print_pass(f"{file_path} exists")
        else:
            print_fail(f"{file_path} is missing")
            all_exist = False
    
    # Check if code is modular (not everything in one file)
    main_size = Path("app/main.py").stat().st_size if Path("app/main.py").exists() else 0
    collector_size = Path("app/collector.py").stat().st_size if Path("app/collector.py").exists() else 0
    
    if main_size > 0 and collector_size > 0:
        print_pass("Code is modular (separated into multiple files)")
    else:
        print_fail("Code structure might be too monolithic")
        all_exist = False
    
    return all_exist


def check_env_file():
    """Test 2: Check for .env file setup."""
    print_header("2️⃣  ENVIRONMENT VARIABLES SETUP")
    
    env_example_exists = Path(".env.example").exists()
    env_exists = Path(".env").exists()
    
    if env_example_exists:
        print_pass(".env.example file exists")
    else:
        print_info(".env.example file not found (may be gitignored)")
    
    if env_exists:
        print_pass(".env file exists")
        # Check if it has the required variables
        from dotenv import load_dotenv
        load_dotenv()
        api_id = os.getenv('TELEGRAM_API_ID')
        api_hash = os.getenv('TELEGRAM_API_HASH')
        
        if api_id and api_id != "your_api_id_here":
            print_pass("TELEGRAM_API_ID is set")
        else:
            print_fail("TELEGRAM_API_ID is not set or uses placeholder value")
        
        if api_hash and api_hash != "your_api_hash_here":
            print_pass("TELEGRAM_API_HASH is set")
        else:
            print_fail("TELEGRAM_API_HASH is not set or uses placeholder value")
        
        return api_id and api_hash and api_id != "your_api_id_here" and api_hash != "your_api_hash_here"
    else:
        print_info(".env file not found (you'll need to create it)")
        print_info("Create .env file with TELEGRAM_API_ID and TELEGRAM_API_HASH")
        return False


def check_database():
    """Test 3: Check database creation."""
    print_header("3️⃣  DATABASE CREATION TEST")
    
    db_path = Path("skillpulse.db")
    
    if db_path.exists():
        print_pass(f"Database file exists: {db_path}")
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ["job_posts", "skills", "job_skill"]
            missing_tables = [t for t in expected_tables if t not in tables]
            
            if not missing_tables:
                print_pass(f"All required tables exist: {', '.join(expected_tables)}")
                
                # Check table structures
                for table in expected_tables:
                    cursor.execute(f"PRAGMA table_info({table});")
                    columns = cursor.fetchall()
                    print_info(f"  {table}: {len(columns)} columns")
                
                conn.close()
                return True
            else:
                print_fail(f"Missing tables: {', '.join(missing_tables)}")
                print_info(f"Found tables: {', '.join(tables)}")
                conn.close()
                return False
                
        except Exception as e:
            print_fail(f"Error checking database: {e}")
            return False
    else:
        print_info("Database file doesn't exist yet (will be created on first run)")
        print_info("Run 'uvicorn app.main:app' or 'python run_collector.py' to create it")
        return True  # Not a failure, just not created yet


def check_fastapi_imports():
    """Test 4: Check if FastAPI can be imported and initialized."""
    print_header("4️⃣  FASTAPI IMPORT & INITIALIZATION TEST")
    
    try:
        from app.main import app
        print_pass("FastAPI app can be imported")
        
        # Check if app has expected endpoints
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/jobs", "/skills", "/stats"]
        found_routes = [r for r in expected_routes if r in routes]
        
        print_info(f"Found routes: {', '.join(found_routes)}")
        
        if len(found_routes) >= 3:
            print_pass("Expected API endpoints are defined")
            return True
        else:
            print_fail("Some expected endpoints are missing")
            return False
            
    except Exception as e:
        print_fail(f"Error importing FastAPI app: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_data_extraction():
    """Test 5: Check data extraction functions."""
    print_header("5️⃣  DATA EXTRACTION TEST")
    
    try:
        from app.extractor import extract_salary, extract_skills, extract_job_title
        
        # Test salary extraction
        test_text_salary = "We're offering $50,000 - $80,000 per year"
        salary = extract_salary(test_text_salary)
        if salary:
            print_pass(f"Salary extraction works (found: {salary})")
        else:
            print_fail("Salary extraction returned None for test text")
            return False
        
        # Test skill extraction
        test_text_skills = "Looking for a Python developer with React and Django experience"
        skills = extract_skills(test_text_skills)
        if skills and len(skills) > 0:
            print_pass(f"Skill extraction works (found: {', '.join(list(skills)[:3])})")
        else:
            print_fail("Skill extraction returned no skills for test text")
            return False
        
        # Test job title extraction
        test_text_title = "Hiring: Senior Backend Developer"
        title = extract_job_title(test_text_title)
        if title:
            print_pass(f"Job title extraction works (found: {title})")
        else:
            print_info("Job title extraction returned None (may be acceptable for some texts)")
        
        return True
        
    except Exception as e:
        print_fail(f"Error testing extraction functions: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_database_data():
    """Test 6: Check if database has data."""
    print_header("6️⃣  DATABASE DATA TEST")
    
    db_path = Path("skillpulse.db")
    
    if not db_path.exists():
        print_info("Database doesn't exist yet - skipping data checks")
        return True
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check job posts count
        cursor.execute("SELECT COUNT(*) FROM job_posts;")
        job_count = cursor.fetchone()[0]
        
        if job_count > 0:
            print_pass(f"Database has {job_count} job posts")
            
            # Check jobs with salary
            cursor.execute("SELECT COUNT(*) FROM job_posts WHERE salary IS NOT NULL;")
            salary_count = cursor.fetchone()[0]
            print_info(f"  Jobs with salary: {salary_count} ({salary_count/job_count*100:.1f}%)")
            
            # Check jobs with title
            cursor.execute("SELECT COUNT(*) FROM job_posts WHERE job_title IS NOT NULL;")
            title_count = cursor.fetchone()[0]
            print_info(f"  Jobs with title: {title_count} ({title_count/job_count*100:.1f}%)")
            
            # Check skills count
            cursor.execute("SELECT COUNT(*) FROM skills;")
            skill_count = cursor.fetchone()[0]
            print_info(f"  Unique skills: {skill_count}")
            
            # Check job_skills relationships
            cursor.execute("SELECT COUNT(*) FROM job_skill;")
            relationship_count = cursor.fetchone()[0]
            print_info(f"  Job-skill relationships: {relationship_count}")
            
            if job_count >= 50:
                print_pass(f"Job count meets Day 1 target (≥50)")
            else:
                print_info(f"Job count is {job_count} (target: ≥50) - run collector to get more")
            
        else:
            print_info("Database exists but has no job posts yet")
            print_info("Run the collector to fetch data: python run_collector.py")
        
        conn.close()
        return True
        
    except Exception as e:
        print_fail(f"Error checking database data: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_readme():
    """Test 7: Check README quality."""
    print_header("7️⃣  README & DOCUMENTATION TEST")
    
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print_fail("README.md is missing")
        return False
    
    readme_content = readme_path.read_text(encoding='utf-8')
    
    required_sections = [
        "Setup",
        "Telegram",
        "Environment",
        "FastAPI",
        "collector",
    ]
    
    found_sections = 0
    for section in required_sections:
        if section.lower() in readme_content.lower():
            found_sections += 1
    
    if found_sections >= 4:
        print_pass("README contains required setup instructions")
        return True
    else:
        print_fail(f"README might be missing some required sections")
        return False


def main():
    """Run all tests."""
    print("\n" + "🧪" * 35)
    print("  DAY 1 VERIFICATION & TESTING SCRIPT")
    print("🧪" * 35)
    
    results = {}
    
    # Run tests
    results['structure'] = check_structure()
    results['env'] = check_env_file()
    results['database'] = check_database()
    results['fastapi'] = check_fastapi_imports()
    results['extraction'] = check_data_extraction()
    results['data'] = check_database_data()
    results['readme'] = check_readme()
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name.upper()}")
    
    print(f"\n{'='*70}")
    print(f"  RESULTS: {passed_tests}/{total_tests} tests passed")
    print(f"{'='*70}\n")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your Day 1 implementation looks good!")
    elif passed_tests >= total_tests - 1:
        print("✅ MOSTLY PASSED! Review any failures above.")
    else:
        print("⚠️  SOME TESTS FAILED. Please review and fix the issues above.")
    
    print("\n📝 NEXT STEPS:")
    print("  1. If FastAPI test passed, try running: uvicorn app.main:app --reload")
    print("  2. If database test passed, check tables: sqlite3 skillpulse.db .tables")
    print("  3. If env test failed, create .env file with Telegram credentials")
    print("  4. If data test failed, run: python run_collector.py")
    print("  5. Open http://localhost:8000/docs in browser to test FastAPI\n")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

