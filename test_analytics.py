"""
Simple test script for analytics functions.
Run after installing dependencies: pip install -r requirements.txt
"""
from app.analytics import parse_salary

def test_parse_salary():
    """Test salary parsing function."""
    test_cases = [
        ('55,000 - 70,000', 62500),
        ('1,400 USD', 1400),
        ('50k-80k', 65000),
        ('100k', 100000),
        ('20,000 – 40,000', 30000),
        ('80,000 – 120,000', 100000),
    ]
    
    print("Testing salary parsing...")
    all_passed = True
    
    for salary_str, expected in test_cases:
        result = parse_salary(salary_str)
        status = "✅" if result and abs(result - expected) < 1 else "❌"
        print(f"{status} {salary_str:30} -> {result} (expected: {expected})")
        if not result or abs(result - expected) >= 1:
            all_passed = False
    
    if all_passed:
        print("\n✅ All salary parsing tests passed!")
    else:
        print("\n❌ Some tests failed")
    
    return all_passed

if __name__ == "__main__":
    test_parse_salary()

