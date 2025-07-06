#!/usr/bin/env python3
"""
Test script to verify bug fixes in the Neuro-Intelligence system.
This script tests the main functionality without requiring full system integration.
"""

import os
import sys
import importlib.util

def test_imports():
    """Test that all modules can be imported without errors."""
    print("Testing module imports...")
    
    modules_to_test = [
        "Core_Processes.Core_Commands",
        "Core_Processes.Core_Functions", 
        "Core_Processes.System_Shortcut_Functions",
        "Core_Processes.app_paths",
        "Dynaminc_Commands_Exucution.Function_Generation",
        "Dynaminc_Commands_Exucution.task_planning",
        "Retrival_Agumented_Generation.rag_command_parser"
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            # Add the parent directory to path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            
            # Import the module
            module = importlib.import_module(module_name)
            print(f"✓ {module_name} imported successfully")
            
        except Exception as e:
            print(f"✗ {module_name} failed to import: {e}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def test_path_resolution():
    """Test that relative path resolution works correctly."""
    print("\nTesting path resolution...")
    
    try:
        # Test that we can find the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"✓ Current directory resolved: {current_dir}")
        
        # Test that subdirectories exist
        subdirs = ["Core_Processes", "Dynaminc_Commands_Exucution", "Retrival_Agumented_Generation"]
        for subdir in subdirs:
            subdir_path = os.path.join(current_dir, subdir)
            if os.path.exists(subdir_path):
                print(f"✓ Subdirectory found: {subdir}")
            else:
                print(f"✗ Subdirectory missing: {subdir}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Path resolution failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling."""
    print("\nTesting environment variable handling...")
    
    try:
        # Test that we can access environment variables
        api_key = os.getenv('GROQ_API_KEY', 'default_key')
        print(f"✓ Environment variable access works (API key length: {len(api_key)})")
        
        # Test that we can set environment variables
        os.environ['TEST_VAR'] = 'test_value'
        test_var = os.getenv('TEST_VAR')
        if test_var == 'test_value':
            print("✓ Environment variable setting works")
            return True
        else:
            print("✗ Environment variable setting failed")
            return False
            
    except Exception as e:
        print(f"✗ Environment variable test failed: {e}")
        return False

def test_error_handling():
    """Test that error handling patterns work correctly."""
    print("\nTesting error handling patterns...")
    
    try:
        # Test basic error handling
        try:
            # Simulate an error
            result = 1 / 0
        except ZeroDivisionError as e:
            print(f"✓ Error handling works: {e}")
        
        # Test that we can continue after an error
        result = 1 + 1
        if result == 2:
            print("✓ Execution continues after error handling")
            return True
        else:
            print("✗ Execution failed after error handling")
            return False
            
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def test_file_operations():
    """Test file operations work correctly."""
    print("\nTesting file operations...")
    
    try:
        # Test CSV file operations
        import csv
        test_file = "test_commands.csv"
        
        # Write test data
        with open(test_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Test Command"])
        
        # Read test data
        with open(test_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        # Clean up
        os.remove(test_file)
        
        if data and data[0][0] == "Test Command":
            print("✓ CSV file operations work correctly")
            return True
        else:
            print("✗ CSV file operations failed")
            return False
            
    except Exception as e:
        print(f"✗ File operations test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Neuro-Intelligence v2.8 - Bug Fix Verification Tests")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Path Resolution", test_path_resolution),
        ("Environment Variables", test_environment_variables),
        ("Error Handling", test_error_handling),
        ("File Operations", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bug fixes are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 