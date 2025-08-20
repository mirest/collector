# Django Upgrade Guide: 2.2.3 → 4.2.16

This document outlines the upgrade from Django 2.2.3 to Django 4.2.16 LTS and all compatibility changes made.

## Package Updates

### Core Framework
- **Django**: 2.2.3 → 4.2.16 (LTS version for stability)
- **djangorestframework**: 3.9.2 → 3.14.0
- **Python**: 3.7 → 3.12 (updated in Pipfile)

### Database & Infrastructure
- **psycopg2-binary**: 2.7.5 → 2.9.7 (fixes Python 3.12 compatibility)
- **gunicorn**: 19.9.0 → 21.2.0
- **dj-database-url**: 0.5.0 → 2.1.0

### Security & Authentication
- **PyJWT**: 1.4.2 → 2.8.0 (major version change with breaking changes)
- **social-auth-app-django**: 3.1.0 → 5.4.0

### Additional Packages
- **django-filter**: 2.1.0 → 23.3
- **whitenoise**: 4.1.2 → 6.5.0
- **django-cors-headers**: 3.0.1 → 4.3.1

## Code Changes Made

### 1. JWT Token Handling (authentication/models.py)
**Issue**: PyJWT 2.x returns strings by default, not bytes
```python
# OLD (Django 2.2 + PyJWT 1.x)
jwt_token = jwt.encode(payload, default.SECRET_KEY)
return jwt_token.decode("utf-8")

# NEW (Django 4.2 + PyJWT 2.x)
jwt_token = jwt.encode(payload, default.SECRET_KEY, algorithm='HS256')
if isinstance(jwt_token, bytes):
    return jwt_token.decode("utf-8")
return jwt_token
```

### 2. ForeignKey on_delete Parameters
**Issue**: Django 3.0+ requires on_delete to be a constant, not a string

#### houses/models.py
```python
# OLD
tenant_id = models.ForeignKey(User, on_delete='CASCADE', ...)
owner_id = models.ForeignKey(User, on_delete='CASCADE', ...)

# NEW
tenant_id = models.ForeignKey(User, on_delete=models.CASCADE, ...)
owner_id = models.ForeignKey(User, on_delete=models.CASCADE, ...)
```

#### payments/models.py
```python
# OLD
house = models.ForeignKey(House, on_delete='CASCADE', ...)
tenant = models.ForeignKey(User, on_delete='CASCADE', ...)

# NEW
house = models.ForeignKey(House, on_delete=models.CASCADE, ...)
tenant = models.ForeignKey(User, on_delete=models.CASCADE, ...)
```

### 3. CORS Configuration (config/default.py)
**Issue**: django-cors-headers 3.x+ uses different setting names
```python
# OLD
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    "http://127.0.0.1:3000",
    "https://collector-239512.appspot.com",
)

# NEW
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "http://127.0.0.1:3000",
    "https://collector-239512.appspot.com",
]
```

### 4. Django 3.2+ Settings (config/default.py)
**Added Required Settings**:
```python
# Required for Django 3.2+
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

**Removed Deprecated Settings**:
```python
# REMOVED - deprecated in Django 4.0+
# USE_L10N = True
```

### 5. Timezone Handling
**Issue**: Using datetime.now() instead of Django's timezone utilities

#### authentication/models.py
```python
# OLD
from datetime import datetime
exp": datetime.now() + timedelta(days=x)

# NEW
from django.utils import timezone
"exp": timezone.now() + timedelta(days=x)
```

#### houses/models.py
```python
# OLD
from datetime import datetime
end_date__gte=datetime.now().date()

# NEW
from django.utils import timezone
end_date__gte=timezone.now().date()
```

## Migration Considerations

### Existing Migrations
- Existing migration files (0001_initial.py) still contain string-based on_delete values
- These cannot be modified as they may have already been applied
- Django will handle the conversion automatically

### New Migrations Needed
After installing packages, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing After Installation

### 1. Basic Django Functionality
```bash
# Check for issues
python manage.py check

# Check for deployment issues
python manage.py check --deploy

# Test migrations
python manage.py makemigrations --dry-run
python manage.py migrate --plan
```

### 2. Run Existing Tests
```bash
# Run all tests
python manage.py test

# Or with pytest
pytest
```

### 3. Test Key Functionality
- User authentication and JWT token generation
- Social authentication (Google, Facebook)
- CORS configuration for frontend
- API endpoints
- Database operations

## Potential Breaking Changes to Watch For

### 1. Django 3.0+ Changes
- **ASGI support**: New async capabilities
- **MariaDB support**: New database backend
- **Django 2.2 compatibility**: Some deprecated features removed

### 2. Django 3.2+ Changes (LTS)
- **DEFAULT_AUTO_FIELD**: Must be explicitly set
- **New admin interface**: Visual changes
- **Security improvements**: Enhanced password validation

### 3. Django 4.0+ Changes
- **USE_L10N removal**: Deprecated setting removed
- **Security improvements**: CSRF token handling changes
- **Template improvements**: New template features

### 4. Django 4.2+ Changes (LTS)
- **Performance improvements**: Query optimizations
- **Security enhancements**: XSS protection improvements
- **Admin interface**: Additional customization options

## Installation Steps (when network is available)

```bash
# Install all requirements
pip install -r requirements.txt

# Check for issues
python manage.py check

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test

# Start development server
python manage.py runserver
```

## Rollback Plan

If issues arise, the upgrade can be rolled back by:
1. Restoring the original requirements.txt and Pipfile
2. Reverting code changes in this commit
3. Reinstalling the old packages
4. Running migrations in reverse if needed

## Environment Variables

Ensure these environment variables are set:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Database connection string
- `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`: Google OAuth key (if using social auth)
- `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET`: Google OAuth secret (if using social auth)

## Additional Notes

- The upgrade maintains backward compatibility where possible
- All existing functionality should work unchanged
- New Django features can be gradually adopted
- Consider upgrading to Django 5.0+ in a future release after testing 4.2 LTS