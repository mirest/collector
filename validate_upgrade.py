#!/usr/bin/env python
"""
Django Upgrade Validation Script

This script performs basic validation that the Django upgrade was successful.
Run this after installing the new packages and running migrations.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def validate_django_upgrade():
    """Validate that the Django upgrade was successful."""
    
    print("🚀 Django Upgrade Validation Starting...")
    print("=" * 50)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.default')
    
    try:
        django.setup()
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Test 1: Check Django version
    print(f"✅ Django version: {django.get_version()}")
    
    # Test 2: Check database connection
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Test 3: Check if models can be imported
    try:
        from authentication.models import User
        from houses.models import House
        from payments.models import Invoices
        print("✅ All models imported successfully")
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False
    
    # Test 4: Check JWT token functionality
    try:
        user = User(username='test', email='test@example.com')
        token = user.token()
        if isinstance(token, str):
            print("✅ JWT token generation successful")
        else:
            print(f"❌ JWT token generation returned wrong type: {type(token)}")
            return False
    except Exception as e:
        print(f"❌ JWT token generation failed: {e}")
        return False
    
    # Test 5: Check CORS settings
    try:
        from django.conf import settings
        if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
            print("✅ CORS settings updated correctly")
        else:
            print("❌ CORS settings not found")
            return False
    except Exception as e:
        print(f"❌ CORS settings check failed: {e}")
        return False
    
    # Test 6: Check DEFAULT_AUTO_FIELD setting
    try:
        from django.conf import settings
        if hasattr(settings, 'DEFAULT_AUTO_FIELD'):
            print("✅ DEFAULT_AUTO_FIELD setting found")
        else:
            print("❌ DEFAULT_AUTO_FIELD setting missing")
            return False
    except Exception as e:
        print(f"❌ DEFAULT_AUTO_FIELD check failed: {e}")
        return False
    
    print("=" * 50)
    print("🎉 All validation tests passed!")
    print("\nNext steps:")
    print("1. Run: python manage.py check")
    print("2. Run: python manage.py check --deploy")
    print("3. Run: python manage.py test")
    print("4. Run: python manage.py runserver")
    return True

def run_django_checks():
    """Run Django's built-in check system."""
    print("\n🔍 Running Django checks...")
    
    try:
        # Run basic checks
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Django checks passed")
        
        # Run deployment checks
        execute_from_command_line(['manage.py', 'check', '--deploy'])
        print("✅ Django deployment checks passed")
        
    except SystemExit as e:
        if e.code == 0:
            print("✅ Django checks completed successfully")
        else:
            print(f"❌ Django checks failed with code: {e.code}")
            return False
    except Exception as e:
        print(f"❌ Django checks failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = True
    
    try:
        success &= validate_django_upgrade()
        success &= run_django_checks()
    except KeyboardInterrupt:
        print("\n❌ Validation interrupted by user")
        success = False
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        success = False
    
    if success:
        print("\n🎉 Django upgrade validation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Django upgrade validation failed!")
        sys.exit(1)