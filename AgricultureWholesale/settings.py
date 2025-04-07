# Allow Vercel domain and localhost
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', '127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For Vercel deployment
if os.environ.get('VERCEL'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    # Vercel has ephemeral filesystem - can't use SQLite in production
    # Consider using a cloud database like PostgreSQL on production

# Static files (CSS, JavaScript, Images) 